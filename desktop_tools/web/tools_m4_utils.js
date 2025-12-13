/* 工具箱（M4）通用算法工具：哈希（MD5 / SHA-256）
 *
 * 设计目标：
 * - 纯算法、无 DOM 依赖，便于浏览器与 Node 环境复用与单元测试
 * - 输入统一按 UTF-8 字节序列处理
 * - 输出统一为小写 Hex
 */
(function (root, factory) {
    if (typeof module !== 'undefined' && module.exports) {
        module.exports = factory();
    } else {
        root.DogToolboxM4Utils = factory();
    }
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
    'use strict';

    function isNodeEnv() {
        return typeof process !== 'undefined' && process.versions && process.versions.node;
    }

    function utf8ToBytes(text) {
        const s = String(text ?? '');
        if (typeof TextEncoder !== 'undefined') {
            return new TextEncoder().encode(s);
        }
        if (isNodeEnv()) {
            return Uint8Array.from(Buffer.from(s, 'utf8'));
        }
        // 兼容极少数环境：使用 encodeURIComponent 转换为 UTF-8 字节
        const escaped = unescape(encodeURIComponent(s)); // eslint-disable-line no-undef
        const bytes = new Uint8Array(escaped.length);
        for (let i = 0; i < escaped.length; i++) {
            bytes[i] = escaped.charCodeAt(i) & 0xff;
        }
        return bytes;
    }

    function bytesToHex(bytes) {
        const u8 = bytes instanceof Uint8Array ? bytes : Uint8Array.from(bytes || []);
        let out = '';
        for (let i = 0; i < u8.length; i++) {
            out += u8[i].toString(16).padStart(2, '0');
        }
        return out;
    }

    // ==================== MD5 ====================
    function rotl32(x, n) {
        return ((x << n) | (x >>> (32 - n))) >>> 0;
    }

    function add32(a, b) {
        return (a + b) >>> 0;
    }

    const MD5_S = [
        7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
        5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20,
        4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
        6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21
    ];

    const MD5_K = (() => {
        const k = new Array(64);
        for (let i = 0; i < 64; i++) {
            k[i] = Math.floor(Math.abs(Math.sin(i + 1)) * 0x100000000) >>> 0;
        }
        return k;
    })();

    function md5Bytes(bytes) {
        const input = bytes instanceof Uint8Array ? bytes : Uint8Array.from(bytes || []);
        const len = input.length;
        const bitLen = len * 8;

        // 追加 0x80 + padding + 64bit 长度（小端）
        const withOne = len + 1;
        const mod = withOne % 64;
        const padLen = mod <= 56 ? (56 - mod) : (56 + 64 - mod);
        const totalLen = len + 1 + padLen + 8;

        const buffer = new Uint8Array(totalLen);
        buffer.set(input);
        buffer[len] = 0x80;

        const bitLenLo = bitLen >>> 0;
        const bitLenHi = Math.floor(bitLen / 0x100000000) >>> 0;
        // 小端写入
        for (let i = 0; i < 4; i++) buffer[totalLen - 8 + i] = (bitLenLo >>> (8 * i)) & 0xff;
        for (let i = 0; i < 4; i++) buffer[totalLen - 4 + i] = (bitLenHi >>> (8 * i)) & 0xff;

        let a0 = 0x67452301;
        let b0 = 0xefcdab89;
        let c0 = 0x98badcfe;
        let d0 = 0x10325476;

        const M = new Array(16);
        for (let offset = 0; offset < buffer.length; offset += 64) {
            for (let i = 0; i < 16; i++) {
                const idx = offset + i * 4;
                M[i] = (
                    buffer[idx] |
                    (buffer[idx + 1] << 8) |
                    (buffer[idx + 2] << 16) |
                    (buffer[idx + 3] << 24)
                ) >>> 0;
            }

            let a = a0;
            let b = b0;
            let c = c0;
            let d = d0;

            for (let i = 0; i < 64; i++) {
                let f, g;
                if (i < 16) {
                    f = (b & c) | (~b & d);
                    g = i;
                } else if (i < 32) {
                    f = (d & b) | (~d & c);
                    g = (5 * i + 1) % 16;
                } else if (i < 48) {
                    f = b ^ c ^ d;
                    g = (3 * i + 5) % 16;
                } else {
                    f = c ^ (b | ~d);
                    g = (7 * i) % 16;
                }

                const tmp = d;
                d = c;
                c = b;

                const sum = add32(add32(add32(a, f >>> 0), MD5_K[i]), M[g]);
                b = add32(b, rotl32(sum, MD5_S[i]));
                a = tmp;
            }

            a0 = add32(a0, a);
            b0 = add32(b0, b);
            c0 = add32(c0, c);
            d0 = add32(d0, d);
        }

        const out = new Uint8Array(16);
        const words = [a0, b0, c0, d0];
        for (let wi = 0; wi < words.length; wi++) {
            const w = words[wi];
            const base = wi * 4;
            out[base] = w & 0xff;
            out[base + 1] = (w >>> 8) & 0xff;
            out[base + 2] = (w >>> 16) & 0xff;
            out[base + 3] = (w >>> 24) & 0xff;
        }
        return out;
    }

    function md5HexUtf8(text) {
        return bytesToHex(md5Bytes(utf8ToBytes(text)));
    }

    // ==================== SHA-256 ====================
    const SHA256_K = [
        0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
        0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
        0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
        0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
        0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
        0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
        0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
        0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
    ];

    function rotr32(x, n) {
        return ((x >>> n) | (x << (32 - n))) >>> 0;
    }

    function sha256Bytes(bytes) {
        const input = bytes instanceof Uint8Array ? bytes : Uint8Array.from(bytes || []);
        const len = input.length;
        const bitLen = len * 8;

        const withOne = len + 1;
        const mod = withOne % 64;
        const padLen = mod <= 56 ? (56 - mod) : (56 + 64 - mod);
        const totalLen = len + 1 + padLen + 8;

        const buffer = new Uint8Array(totalLen);
        buffer.set(input);
        buffer[len] = 0x80;

        const bitLenHi = Math.floor(bitLen / 0x100000000) >>> 0;
        const bitLenLo = bitLen >>> 0;
        // 大端写入
        buffer[totalLen - 8] = (bitLenHi >>> 24) & 0xff;
        buffer[totalLen - 7] = (bitLenHi >>> 16) & 0xff;
        buffer[totalLen - 6] = (bitLenHi >>> 8) & 0xff;
        buffer[totalLen - 5] = bitLenHi & 0xff;
        buffer[totalLen - 4] = (bitLenLo >>> 24) & 0xff;
        buffer[totalLen - 3] = (bitLenLo >>> 16) & 0xff;
        buffer[totalLen - 2] = (bitLenLo >>> 8) & 0xff;
        buffer[totalLen - 1] = bitLenLo & 0xff;

        let h0 = 0x6a09e667;
        let h1 = 0xbb67ae85;
        let h2 = 0x3c6ef372;
        let h3 = 0xa54ff53a;
        let h4 = 0x510e527f;
        let h5 = 0x9b05688c;
        let h6 = 0x1f83d9ab;
        let h7 = 0x5be0cd19;

        const w = new Array(64);
        for (let offset = 0; offset < buffer.length; offset += 64) {
            for (let i = 0; i < 16; i++) {
                const idx = offset + i * 4;
                w[i] = (
                    (buffer[idx] << 24) |
                    (buffer[idx + 1] << 16) |
                    (buffer[idx + 2] << 8) |
                    buffer[idx + 3]
                ) >>> 0;
            }
            for (let i = 16; i < 64; i++) {
                const s0 = (rotr32(w[i - 15], 7) ^ rotr32(w[i - 15], 18) ^ (w[i - 15] >>> 3)) >>> 0;
                const s1 = (rotr32(w[i - 2], 17) ^ rotr32(w[i - 2], 19) ^ (w[i - 2] >>> 10)) >>> 0;
                w[i] = add32(add32(add32(w[i - 16], s0), w[i - 7]), s1);
            }

            let a = h0;
            let b = h1;
            let c = h2;
            let d = h3;
            let e = h4;
            let f = h5;
            let g = h6;
            let h = h7;

            for (let i = 0; i < 64; i++) {
                const S1 = (rotr32(e, 6) ^ rotr32(e, 11) ^ rotr32(e, 25)) >>> 0;
                const ch = ((e & f) ^ (~e & g)) >>> 0;
                const temp1 = add32(add32(add32(add32(h, S1), ch), SHA256_K[i]), w[i]);
                const S0 = (rotr32(a, 2) ^ rotr32(a, 13) ^ rotr32(a, 22)) >>> 0;
                const maj = ((a & b) ^ (a & c) ^ (b & c)) >>> 0;
                const temp2 = add32(S0, maj);

                h = g;
                g = f;
                f = e;
                e = add32(d, temp1);
                d = c;
                c = b;
                b = a;
                a = add32(temp1, temp2);
            }

            h0 = add32(h0, a);
            h1 = add32(h1, b);
            h2 = add32(h2, c);
            h3 = add32(h3, d);
            h4 = add32(h4, e);
            h5 = add32(h5, f);
            h6 = add32(h6, g);
            h7 = add32(h7, h);
        }

        const out = new Uint8Array(32);
        const words = [h0, h1, h2, h3, h4, h5, h6, h7];
        for (let wi = 0; wi < words.length; wi++) {
            const wv = words[wi];
            const base = wi * 4;
            out[base] = (wv >>> 24) & 0xff;
            out[base + 1] = (wv >>> 16) & 0xff;
            out[base + 2] = (wv >>> 8) & 0xff;
            out[base + 3] = wv & 0xff;
        }
        return out;
    }

    function sha256HexUtf8(text) {
        return bytesToHex(sha256Bytes(utf8ToBytes(text)));
    }

    // ==================== 对外 API ====================
    function hashHexUtf8(text, algorithm) {
        const algo = String(algorithm || '').toLowerCase();
        if (algo === 'md5') return md5HexUtf8(text);
        if (algo === 'sha256' || algo === 'sha-256') return sha256HexUtf8(text);
        throw new Error('不支持的算法：' + (algorithm || ''));
    }

    return {
        md5HexUtf8,
        sha256HexUtf8,
        hashHexUtf8
    };
});

