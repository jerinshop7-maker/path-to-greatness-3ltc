/*
 * sweep.c -- L1 padding-oracle brute forcer for the Path to Greatness segments.
 *
 * The AES key is 32 bytes = two clue answers concatenated. The tool takes a
 * 32-byte template and a 32-char mask and tries every combination:
 *   mask char '.'  -> try printable ASCII 0x20..0x7e at that position
 *   mask char '0'  -> try ASCII digits 0x30..0x39 at that position
 *   mask char 'r'  -> mirror the byte from 8 positions earlier (block written twice)
 *   anything else  -> position fixed to the template byte
 * A hit is a key that decrypts the segment ciphertext to a plaintext whose
 * last 8 bytes are all 0x08 (PKCS7 for one block holding 8 useful bytes).
 *
 * usage: sweep <segid 1-4> <template32chars> <mask32chars>
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

/* ---------------- minimal AES-256 encryption (FIPS-197) ---------------- */
static const uint8_t SBOX[256] = {
0x63,0x7c,0x77,0x7b,0xf2,0x6b,0x6f,0xc5,0x30,0x01,0x67,0x2b,0xfe,0xd7,0xab,0x76,
0xca,0x82,0xc9,0x7d,0xfa,0x59,0x47,0xf0,0xad,0xd4,0xa2,0xaf,0x9c,0xa4,0x72,0xc0,
0xb7,0xfd,0x93,0x26,0x36,0x3f,0xf7,0xcc,0x34,0xa5,0xe5,0xf1,0x71,0xd8,0x31,0x15,
0x04,0xc7,0x23,0xc3,0x18,0x96,0x05,0x9a,0x07,0x12,0x80,0xe2,0xeb,0x27,0xb2,0x75,
0x09,0x83,0x2c,0x1a,0x1b,0x6e,0x5a,0xa0,0x52,0x3b,0xd6,0xb3,0x29,0xe3,0x2f,0x84,
0x53,0xd1,0x00,0xed,0x20,0xfc,0xb1,0x5b,0x6a,0xcb,0xbe,0x39,0x4a,0x4c,0x58,0xcf,
0xd0,0xef,0xaa,0xfb,0x43,0x4d,0x33,0x85,0x45,0xf9,0x02,0x7f,0x50,0x3c,0x9f,0xa8,
0x51,0xa3,0x40,0x8f,0x92,0x9d,0x38,0xf5,0xbc,0xb6,0xda,0x21,0x10,0xff,0xf3,0xd2,
0xcd,0x0c,0x13,0xec,0x5f,0x97,0x44,0x17,0xc4,0xa7,0x7e,0x3d,0x64,0x5d,0x19,0x73,
0x60,0x81,0x4f,0xdc,0x22,0x2a,0x90,0x88,0x46,0xee,0xb8,0x14,0xde,0x5e,0x0b,0xdb,
0xe0,0x32,0x3a,0x0a,0x49,0x06,0x24,0x5c,0xc2,0xd3,0xac,0x62,0x91,0x95,0xe4,0x79,
0xe7,0xc8,0x37,0x6d,0x8d,0xd5,0x4e,0xa9,0x6c,0x56,0xf4,0xea,0x65,0x7a,0xae,0x08,
0xba,0x78,0x25,0x2e,0x1c,0xa6,0xb4,0xc6,0xe8,0xdd,0x74,0x1f,0x4b,0xbd,0x8b,0x8a,
0x70,0x3e,0xb5,0x66,0x48,0x03,0xf6,0x0e,0x61,0x35,0x57,0xb9,0x86,0xc1,0x1d,0x9e,
0xe1,0xf8,0x98,0x11,0x69,0xd9,0x8e,0x94,0x9b,0x1e,0x87,0xe9,0xce,0x55,0x28,0xdf,
0x8c,0xa1,0x89,0x0d,0xbf,0xe6,0x42,0x68,0x41,0x99,0x2d,0x0f,0xb0,0x54,0xbb,0x16};
static uint8_t MUL1[256], MUL2[256], MUL3[256], MUL9[256], MUL11[256], MUL13[256], MUL14[256];
static void build_tables(void){
    /* Pass 1: 2x must be complete before 4x = 2x(2x) can be tabulated. */
    for(int x=0;x<256;x++)
        MUL1[x]=(uint8_t)((x<<1)^((x&0x80)?0x1b:0));
    for(int x=0;x<256;x++){
        MUL2[x]=MUL1[MUL1[x]];          /* 4x */
        MUL3[x]=(uint8_t)(MUL1[x]^x);   /* 3x = 2x ^ x */
    }
    /* Pass 2: 8x = 2x(4x) needs the finished 4x table. */
    for(int x=0;x<256;x++){
        uint8_t m8=MUL1[MUL2[x]];       /* 8x */
        MUL9[x] =(uint8_t)(m8^x);               /* 9x  = 8x ^ x   */
        MUL11[x]=(uint8_t)(m8^MUL1[x]^x);       /* 11x = 8x ^ 2x ^ x */
        MUL13[x]=(uint8_t)(m8^MUL2[x]^x);       /* 13x = 8x ^ 4x ^ x */
        MUL14[x]=(uint8_t)(m8^MUL2[x]^MUL1[x]); /* 14x = 8x ^ 4x ^ 2x */
    }
}
static void aes256_expand(const uint8_t*key,uint8_t rk[240]){
    static const uint8_t RCON[11]={0,0x01,0x02,0x04,0x08,0x10,0x20,0x40,0x80,0x1b,0x36};
    memcpy(rk,key,32);
    int i=8;
    while(i<60){
        uint8_t t[4]={rk[4*i-4],rk[4*i-3],rk[4*i-2],rk[4*i-1]};
        if(i%8==0){
            uint8_t tmp=t[0];
            t[0]=SBOX[t[1]]^RCON[i/8]; t[1]=SBOX[t[2]]; t[2]=SBOX[t[3]]; t[3]=SBOX[tmp];
        } else if(i%8==4){
            for(int a=0;a<4;a++) t[a]=SBOX[t[a]];
        }
        rk[4*i]=rk[4*(i-8)]^t[0];
        rk[4*i+1]=rk[4*(i-8)+1]^t[1];
        rk[4*i+2]=rk[4*(i-8)+2]^t[2];
        rk[4*i+3]=rk[4*(i-8)+3]^t[3];
        i++;
    }
}
/* InvSubBytes + InvShiftRows in one pass (flat layout, row=i%4). */
static const uint8_t ISBOX[256] = {
0x52,0x09,0x6a,0xd5,0x30,0x36,0xa5,0x38,0xbf,0x40,0xa3,0x9e,0x81,0xf3,0xd7,0xfb,
0x7c,0xe3,0x39,0x82,0x9b,0x2f,0xff,0x87,0x34,0x8e,0x43,0x44,0xc4,0xde,0xe9,0xcb,
0x54,0x7b,0x94,0x32,0xa6,0xc2,0x23,0x3d,0xee,0x4c,0x95,0x0b,0x42,0xfa,0xc3,0x4e,
0x08,0x2e,0xa1,0x66,0x28,0xd9,0x24,0xb2,0x76,0x5b,0xa2,0x49,0x6d,0x8b,0xd1,0x25,
0x72,0xf8,0xf6,0x64,0x86,0x68,0x98,0x16,0xd4,0xa4,0x5c,0xcc,0x5d,0x65,0xb6,0x92,
0x6c,0x70,0x48,0x50,0xfd,0xed,0xb9,0xda,0x5e,0x15,0x46,0x57,0xa7,0x8d,0x9d,0x84,
0x90,0xd8,0xab,0x00,0x8c,0xbc,0xd3,0x0a,0xf7,0xe4,0x58,0x05,0xb8,0xb3,0x45,0x06,
0xd0,0x2c,0x1e,0x8f,0xca,0x3f,0x0f,0x02,0xc1,0xaf,0xbd,0x03,0x01,0x13,0x8a,0x6b,
0x3a,0x91,0x11,0x41,0x4f,0x67,0xdc,0xea,0x97,0xf2,0xcf,0xce,0xf0,0xb4,0xe6,0x73,
0x96,0xac,0x74,0x22,0xe7,0xad,0x35,0x85,0xe2,0xf9,0x37,0xe8,0x1c,0x75,0xdf,0x6e,
0x47,0xf1,0x1a,0x71,0x1d,0x29,0xc5,0x89,0x6f,0xb7,0x62,0x0e,0xaa,0x18,0xbe,0x1b,
0xfc,0x56,0x3e,0x4b,0xc6,0xd2,0x79,0x20,0x9a,0xdb,0xc0,0xfe,0x78,0xcd,0x5a,0xf4,
0x1f,0xdd,0xa8,0x33,0x88,0x07,0xc7,0x31,0xb1,0x12,0x10,0x59,0x27,0x80,0xec,0x5f,
0x60,0x51,0x7f,0xa9,0x19,0xb5,0x4a,0x0d,0x2d,0xe5,0x7a,0x9f,0x93,0xc9,0x9c,0xef,
0xa0,0xe0,0x3b,0x4d,0xae,0x2a,0xf5,0xb0,0xc8,0xeb,0xbb,0x3c,0x83,0x53,0x99,0x61,
0x17,0x2b,0x04,0x7e,0xba,0x77,0xd6,0x26,0xe1,0x69,0x14,0x63,0x55,0x21,0x0c,0x7d};
static void inv_shift_sub(const uint8_t*s,uint8_t*u){
    /* InvShiftRows (row r moves right by r) then InvSubBytes, flat layout */
    u[0]=ISBOX[s[0]];  u[4]=ISBOX[s[4]];  u[8]=ISBOX[s[8]];   u[12]=ISBOX[s[12]];
    u[1]=ISBOX[s[13]]; u[5]=ISBOX[s[1]];  u[9]=ISBOX[s[5]];   u[13]=ISBOX[s[9]];
    u[2]=ISBOX[s[10]]; u[6]=ISBOX[s[14]]; u[10]=ISBOX[s[2]];  u[14]=ISBOX[s[6]];
    u[3]=ISBOX[s[7]];  u[7]=ISBOX[s[11]]; u[11]=ISBOX[s[15]]; u[15]=ISBOX[s[3]];
}
static void inv_mix_cols(uint8_t*a,uint8_t*b){
    b[0]=(uint8_t)(MUL14[a[0]]^MUL11[a[1]]^MUL13[a[2]]^MUL9[a[3]]);
    b[1]=(uint8_t)(MUL9[a[0]]^MUL14[a[1]]^MUL11[a[2]]^MUL13[a[3]]);
    b[2]=(uint8_t)(MUL13[a[0]]^MUL9[a[1]]^MUL14[a[2]]^MUL11[a[3]]);
    b[3]=(uint8_t)(MUL11[a[0]]^MUL13[a[1]]^MUL9[a[2]]^MUL14[a[3]]);
}
/* AES-256 block DECRYPTION. pt = D(ct). */
static void aes256_decrypt_block(const uint8_t*rk,const uint8_t*in,uint8_t*out){
    uint8_t s[16],u[16],t[16];
    memcpy(s,in,16);
    for(int i=0;i<16;i++) s[i]^=rk[224+i];          /* ARK(Nr=14) */
    for(int r=13;r>=1;r--){
        inv_shift_sub(s,u);
        for(int i=0;i<16;i++) u[i]^=rk[16*r+i];     /* ARK(round) */
        for(int c=0;c<4;c++) inv_mix_cols(u+4*c,t+4*c);
        memcpy(s,t,16);
    }
    inv_shift_sub(s,u);
    for(int i=0;i<16;i++) out[i]=u[i]^rk[i];        /* ARK(0) */
}
static const char* SEG_CT_B64[5] = {NULL,
    "I2c6TXU/Z1oCKnEQTWZUvg==",
    "RWaBo4ChEOM/i+MLy2NUpg==",
    "16GmtUINaYuN7f1RlBO5sQ==",
    "7CZlZjwCMGUb/TZm07b9dg=="};
static const char* SEG_IV[5] = {NULL,
    "few_n_far_btween",
    "nocturnal_sugars",
    "colors_on_leaves",
    "seconds_of_dream"};

static int b64val(int c){
    if(c>='A'&&c<='Z') return c-'A';
    if(c>='a'&&c<='z') return c-'a'+26;
    if(c>='0'&&c<='9') return c-'0'+52;
    if(c=='+') return 62;
    if(c=='/') return 63;
    return -1;
}
static void b64decode(const char*s,uint8_t*out,int*n){
    int acc=0,bits=0,o=0;
    for(const char*p=s;*p&&*p!='=';p++){
        acc=(acc<<6)|b64val(*p); bits+=6;
        if(bits>=8){ bits-=8; out[o++]=(acc>>bits)&0xff; }
    }
    *n=o;
}
static int hexnib(int c){
    if(c>='0'&&c<='9') return c-'0';
    if(c>='a'&&c<='f') return c-'a'+10;
    if(c>='A'&&c<='F') return c-'A'+10;
    return -1;
}
static void hexdecode(const char*s,uint8_t*out){
    size_t n=strlen(s)/2;
    for(size_t i=0;i<n;i++) out[i]=(uint8_t)(hexnib(s[2*i])*16+hexnib(s[2*i+1]));
}

/* ------------------------------- main ---------------------------------- */
int main(int argc,char**argv){
    if(argc==2&&!strcmp(argv[1],"test")){
        /* FIPS-197 SP 800-38A AES-256 ECB vector */
        build_tables();
        uint8_t key[32],pt[16],rk[240],out[16];
        hexdecode("603deb1015ca71be2b73aef0857d77811f352c073b6108d72d9810a30914dff4",key);
        hexdecode("6bc1bee22e409f96e93d7e117393172a",pt);
        aes256_expand(key,rk);
        {
            uint8_t s[16],u[16],t[16];
            memcpy(s,pt,16);
            for(int i=0;i<16;i++) s[i]^=rk[i];
            printf("after ARK0   "); for(int i=0;i<16;i++) printf("%02x",s[i]); printf("\n");
            u[0]=SBOX[s[0]];  u[4]=SBOX[s[4]];  u[8]=SBOX[s[8]];   u[12]=SBOX[s[12]];
            u[1]=SBOX[s[5]];  u[5]=SBOX[s[9]];  u[9]=SBOX[s[13]];  u[13]=SBOX[s[1]];
            u[2]=SBOX[s[10]]; u[6]=SBOX[s[14]]; u[10]=SBOX[s[2]];  u[14]=SBOX[s[6]];
            u[3]=SBOX[s[15]]; u[7]=SBOX[s[3]];  u[11]=SBOX[s[7]];  u[15]=SBOX[s[11]];
            printf("u          "); for(int i=0;i<16;i++) printf("%02x",u[i]); printf("\n");
            printf("MUL1[7b]=%02x MUL3[7e]=%02x MUL1[cd]=%02x MUL3[be]=%02x MUL3[cd]=%02x MUL1[be]=%02x\n",
                   MUL1[0x7b],MUL3[0x7e],MUL1[0xcd],MUL3[0xbe],MUL3[0xcd],MUL1[0xbe]);
            for(int c=0;c<4;c++){
                uint8_t*a=u+4*c;
                t[4*c+0]=(uint8_t)(MUL1[a[0]]^MUL3[a[1]]^a[2]^a[3]);
                t[4*c+1]=(uint8_t)(a[0]^MUL1[a[1]]^MUL3[a[2]]^a[3]);
                t[4*c+2]=(uint8_t)(a[0]^a[1]^MUL1[a[2]]^MUL3[a[3]]);
                t[4*c+3]=(uint8_t)(MUL3[a[0]]^a[1]^a[2]^MUL1[a[3]]);
            }
            printf("after round0 "); for(int i=0;i<16;i++) printf("%02x",t[i]); printf("\n");
        }
        /* full trace: re-run the function logic inline, printing every round */
        {
            uint8_t s[16],u[16],t[16];
            memcpy(s,pt,16);
            for(int r=0;r<13;r++){
                for(int i=0;i<16;i++) s[i]^=rk[16*r+i];
                printf("ARK%02d ",r); for(int i=0;i<16;i++) printf("%02x",s[i]); printf("\n");
                u[0]=SBOX[s[0]];  u[4]=SBOX[s[4]];  u[8]=SBOX[s[8]];   u[12]=SBOX[s[12]];
                u[1]=SBOX[s[5]];  u[5]=SBOX[s[9]];  u[9]=SBOX[s[13]];  u[13]=SBOX[s[1]];
                u[2]=SBOX[s[10]]; u[6]=SBOX[s[14]]; u[10]=SBOX[s[2]];  u[14]=SBOX[s[6]];
                u[3]=SBOX[s[15]]; u[7]=SBOX[s[3]];  u[11]=SBOX[s[7]];  u[15]=SBOX[s[11]];
                for(int c=0;c<4;c++){
                    uint8_t*a=u+4*c;
                    t[4*c+0]=(uint8_t)(MUL1[a[0]]^MUL3[a[1]]^a[2]^a[3]);
                    t[4*c+1]=(uint8_t)(a[0]^MUL1[a[1]]^MUL3[a[2]]^a[3]);
                    t[4*c+2]=(uint8_t)(a[0]^a[1]^MUL1[a[2]]^MUL3[a[3]]);
                    t[4*c+3]=(uint8_t)(MUL3[a[0]]^a[1]^a[2]^MUL1[a[3]]);
                }
                memcpy(s,t,16);
                printf("rnd%02d ",r); for(int i=0;i<16;i++) printf("%02x",s[i]); printf("\n");
            }
            for(int i=0;i<16;i++) s[i]^=rk[208+i];
            printf("ARK13 "); for(int i=0;i<16;i++) printf("%02x",s[i]); printf("\n");
            u[0]=SBOX[s[0]];  u[4]=SBOX[s[4]];  u[8]=SBOX[s[8]];   u[12]=SBOX[s[12]];
            u[1]=SBOX[s[5]];  u[5]=SBOX[s[9]];  u[9]=SBOX[s[13]];  u[13]=SBOX[s[1]];
            u[2]=SBOX[s[10]]; u[6]=SBOX[s[14]]; u[10]=SBOX[s[2]];  u[14]=SBOX[s[6]];
            u[3]=SBOX[s[15]]; u[7]=SBOX[s[3]];  u[11]=SBOX[s[7]];  u[15]=SBOX[s[11]];
            for(int i=0;i<16;i++) out[i]=u[i]^rk[224+i];
            printf("out   "); for(int i=0;i<16;i++) printf("%02x",out[i]); printf("\n");
        }
        printf("expected f3eed1bdb5d2a03c064b5a7e3db181f8\n");
        return 0;
    }
    if(argc!=4&&argc!=5){ fprintf(stderr,"usage: sweep <seg 1-4|test> <template32> <mask32> [ct-b64]\n"); return 2; }
    int seg=atoi(argv[1]);
    if(seg<1||seg>4){ fprintf(stderr,"seg must be 1-4\n"); return 2; }
    const char*tpl=argv[2];
    const char*mask=argv[3];
    if(strlen(tpl)!=32||strlen(mask)!=32){ fprintf(stderr,"template and mask must be 32 chars\n"); return 2; }

    build_tables();
    uint8_t ct[16],iv[16];
    int n; b64decode(SEG_CT_B64[seg],ct,&n);
    if(argc==5) b64decode(argv[4],ct,&n);
    memcpy(iv,SEG_IV[seg],16);

    /* variable positions. 'r' positions mirror the byte 8 earlier, so they
       do not get their own odometer digit. */
    int varpos[32],nvar=0;
    int lo[32],hi[32];
    int mirror[32];
    memset(mirror,0,sizeof(mirror));
    for(int i=0;i<32;i++){
        if(mask[i]=='r'){ mirror[i]=1; continue; }
    }
    for(int i=0;i<32;i++){
        if(mask[i]=='.'){ lo[nvar]=0x20; hi[nvar]=0x7e; varpos[nvar]=i; nvar++; }
        else if(mask[i]=='0'){ lo[nvar]=0x30; hi[nvar]=0x39; varpos[nvar]=i; nvar++; }
        else if(mask[i]=='?'){ lo[nvar]=0x00; hi[nvar]=0xff; varpos[nvar]=i; nvar++; }
    }
    fprintf(stderr,"seg %d, %d variable positions, space=%.3g\n",seg,nvar,1.0);
    double space=1.0; for(int i=0;i<nvar;i++) space*=(hi[i]-lo[i]+1);
    fprintf(stderr,"space = %.4g keys\n",space);

    uint8_t key[32],rk[240],out[16];
    for(int i=0;i<32;i++) key[i]=(uint8_t)tpl[i];
    int idx[32];
    for(int i=0;i<nvar;i++){ key[varpos[i]]=(uint8_t)lo[i]; idx[i]=lo[i]; }

    unsigned long long tried=0;
    int digits=nvar-1;
    for(int i=0;i<32;i++) if(mirror[i]) key[i]=key[i-8];
    for(;;){
        /* test current key: pt = D(ct) ^ iv; need pt[8..15] = 08*8 */
        aes256_expand(key,rk);
        aes256_decrypt_block(rk,ct,out);
        int ok=1;
        for(int i=8;i<16;i++) if((uint8_t)(out[i]^iv[i])!=0x08){ ok=0; break; }
        tried++;
        if(ok){
            /* CBC: p = D(c) xor iv; check the 8 message bytes too (printable) */
            uint8_t pt[16];
            for(int i=0;i<16;i++) pt[i]=out[i]^iv[i];
            printf("HIT key=");
            for(int i=0;i<32;i++) putchar(key[i]>=0x20&&key[i]<0x7f?key[i]:'.');
            printf("  pt8=");
            for(int i=0;i<8;i++) printf("%02x",pt[i]);
            printf("  ascii8=");
            for(int i=0;i<8;i++) putchar(pt[i]>=0x20&&pt[i]<0x7f?pt[i]:'.');
            printf("\n");
            fflush(stdout);
        }
        /* odometer increment */
        int d=digits;
        while(d>=0){
            if(idx[d]<hi[d]){ idx[d]++; key[varpos[d]]=(uint8_t)idx[d]; break; }
            idx[d]=lo[d]; key[varpos[d]]=(uint8_t)lo[d]; d--;
        }
        if(d<0) break;

        /* mirror the 'r' positions from 8 bytes earlier, before the next test */
        for(int i=0;i<32;i++) if(mirror[i]) key[i]=key[i-8];
    }
    fprintf(stderr,"done, %llu keys tried, no hit\n",tried);
    return 1;
}
