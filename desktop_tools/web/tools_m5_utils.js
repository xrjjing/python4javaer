/* 工具箱（M5）通用算法工具：AES/DES（ECB + PKCS7）、Base64/Hex 编解码
 *
 * 设计目标：
 * - 纯算法、无 DOM 依赖，便于浏览器与 Node 环境复用与单元测试
 * - 明文/Key 统一按 UTF-8 转字节
 * - 密文输出支持 Base64 / Hex
 * - 支持 Key 自动调整（不足右补 0x00，超出截断）或严格长度校验
 */
(function (root, factory) {
    if (typeof module !== 'undefined' && module.exports) {
        module.exports = factory();
    } else {
        root.DogToolboxM5Utils = factory();
    }
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
    'use strict';

    function isNodeEnv() {
        return typeof process !== 'undefined' && process.versions && process.versions.node;
    }

    // ==================== 字节/编码工具 ====================
    function utf8ToBytes(text) {
        const s = String(text ?? '');
        if (typeof TextEncoder !== 'undefined') {
            return new TextEncoder().encode(s);
        }
        if (isNodeEnv()) {
            return Uint8Array.from(Buffer.from(s, 'utf8'));
        }
        const escaped = unescape(encodeURIComponent(s)); // eslint-disable-line no-undef
        const bytes = new Uint8Array(escaped.length);
        for (let i = 0; i < escaped.length; i++) bytes[i] = escaped.charCodeAt(i) & 0xff;
        return bytes;
    }

    function bytesToUtf8(bytes) {
        const u8 = bytes instanceof Uint8Array ? bytes : Uint8Array.from(bytes || []);
        if (typeof TextDecoder !== 'undefined') {
            return new TextDecoder('utf-8', { fatal: true }).decode(u8);
        }
        if (isNodeEnv()) {
            return Buffer.from(u8).toString('utf8');
        }
        let s = '';
        for (let i = 0; i < u8.length; i++) s += String.fromCharCode(u8[i]);
        return s;
    }

    function bytesToHex(bytes) {
        const u8 = bytes instanceof Uint8Array ? bytes : Uint8Array.from(bytes || []);
        let out = '';
        for (let i = 0; i < u8.length; i++) out += u8[i].toString(16).padStart(2, '0');
        return out;
    }

    function hexToBytes(hex) {
        const raw = String(hex ?? '').trim().replace(/\s+/g, '');
        if (!raw) return new Uint8Array(0);
        if (raw.length % 2 !== 0) throw new Error('非法 Hex：长度必须为偶数');
        if (!/^[0-9a-fA-F]+$/.test(raw)) throw new Error('非法 Hex：包含非十六进制字符');
        const out = new Uint8Array(raw.length / 2);
        for (let i = 0; i < raw.length; i += 2) {
            out[i / 2] = parseInt(raw.slice(i, i + 2), 16) & 0xff;
        }
        return out;
    }

    function base64EncodeBytes(bytes) {
        const u8 = bytes instanceof Uint8Array ? bytes : Uint8Array.from(bytes || []);
        if (typeof btoa === 'function') {
            let binary = '';
            for (let i = 0; i < u8.length; i++) binary += String.fromCharCode(u8[i]);
            return btoa(binary);
        }
        if (isNodeEnv()) {
            return Buffer.from(u8).toString('base64');
        }
        throw new Error('当前环境不支持 Base64 编码');
    }

    function base64DecodeToBytes(b64) {
        let raw = String(b64 ?? '').trim();
        if (!raw) return new Uint8Array(0);
        raw = raw.replace(/\s+/g, '');
        // 允许缺少 padding
        const mod = raw.length % 4;
        if (mod === 2) raw += '==';
        else if (mod === 3) raw += '=';
        else if (mod === 1) throw new Error('非法 Base64：长度不合法');

        if (!/^[A-Za-z0-9+/=]+$/.test(raw)) throw new Error('非法 Base64：包含不支持的字符');

        if (typeof atob === 'function') {
            const binary = atob(raw);
            const out = new Uint8Array(binary.length);
            for (let i = 0; i < binary.length; i++) out[i] = binary.charCodeAt(i) & 0xff;
            return out;
        }
        if (isNodeEnv()) {
            return Uint8Array.from(Buffer.from(raw, 'base64'));
        }
        throw new Error('当前环境不支持 Base64 解码');
    }

    // ==================== PKCS7 填充 ====================
    function pkcs7Pad(bytes, blockSize) {
        const u8 = bytes instanceof Uint8Array ? bytes : Uint8Array.from(bytes || []);
        const bs = Number(blockSize);
        if (!Number.isFinite(bs) || bs <= 0) throw new Error('blockSize 不合法');
        const padLen = bs - (u8.length % bs || 0);
        const out = new Uint8Array(u8.length + padLen);
        out.set(u8);
        out.fill(padLen & 0xff, u8.length);
        return out;
    }

    function pkcs7Unpad(bytes, blockSize) {
        const u8 = bytes instanceof Uint8Array ? bytes : Uint8Array.from(bytes || []);
        const bs = Number(blockSize);
        if (u8.length === 0 || u8.length % bs !== 0) throw new Error('非法密文长度（非整块）');
        const padLen = u8[u8.length - 1];
        if (padLen <= 0 || padLen > bs) throw new Error('PKCS7 填充不合法');
        for (let i = u8.length - padLen; i < u8.length; i++) {
            if (u8[i] !== padLen) throw new Error('PKCS7 填充不合法');
        }
        return u8.slice(0, u8.length - padLen);
    }

    // ==================== Key 处理 ====================
    function adjustKeyUtf8(keyText, targetLen, autoAdjust) {
        const raw = utf8ToBytes(keyText);
        const t = Number(targetLen);
        if (!Number.isFinite(t) || t <= 0) throw new Error('目标 key 长度不合法');
        if (!autoAdjust) {
            if (raw.length !== t) throw new Error(`key 长度必须为 ${t} 字节（UTF-8）`);
            return raw;
        }
        const out = new Uint8Array(t);
        out.set(raw.slice(0, t));
        return out;
    }

    // ==================== AES（ECB） ====================
    const AES_SBOX = [
        0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
        0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
        0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
        0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
        0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
        0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
        0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
        0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
        0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
        0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
        0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
        0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
        0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
        0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
        0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
        0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
    ];

    const AES_INV_SBOX = [
        0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb,
        0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb,
        0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e,
        0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25,
        0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92,
        0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84,
        0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06,
        0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b,
        0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73,
        0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e,
        0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b,
        0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4,
        0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f,
        0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef,
        0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61,
        0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d
    ];

    const AES_RCON = [
        0x00,
        0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36,
        0x6c, 0xd8, 0xab, 0x4d, 0x9a
    ];

    function xtime(a) {
        return ((a << 1) ^ ((a & 0x80) ? 0x1b : 0x00)) & 0xff;
    }

    function gmul(a, b) {
        let p = 0;
        let aa = a & 0xff;
        let bb = b & 0xff;
        for (let i = 0; i < 8; i++) {
            if (bb & 1) p ^= aa;
            const hi = aa & 0x80;
            aa = (aa << 1) & 0xff;
            if (hi) aa ^= 0x1b;
            bb >>= 1;
        }
        return p & 0xff;
    }

    function subBytes(state) {
        for (let i = 0; i < 16; i++) state[i] = AES_SBOX[state[i]];
    }

    function invSubBytes(state) {
        for (let i = 0; i < 16; i++) state[i] = AES_INV_SBOX[state[i]];
    }

    function shiftRows(state) {
        const t = state.slice();
        state[1] = t[5]; state[5] = t[9]; state[9] = t[13]; state[13] = t[1];
        state[2] = t[10]; state[6] = t[14]; state[10] = t[2]; state[14] = t[6];
        state[3] = t[15]; state[7] = t[3]; state[11] = t[7]; state[15] = t[11];
    }

    function invShiftRows(state) {
        const t = state.slice();
        state[1] = t[13]; state[5] = t[1]; state[9] = t[5]; state[13] = t[9];
        state[2] = t[10]; state[6] = t[14]; state[10] = t[2]; state[14] = t[6];
        state[3] = t[7]; state[7] = t[11]; state[11] = t[15]; state[15] = t[3];
    }

    function mixColumns(state) {
        for (let c = 0; c < 4; c++) {
            const i = c * 4;
            const a0 = state[i], a1 = state[i + 1], a2 = state[i + 2], a3 = state[i + 3];
            const t = a0 ^ a1 ^ a2 ^ a3;
            const u = a0;
            state[i] = (a0 ^ t ^ xtime(a0 ^ a1)) & 0xff;
            state[i + 1] = (a1 ^ t ^ xtime(a1 ^ a2)) & 0xff;
            state[i + 2] = (a2 ^ t ^ xtime(a2 ^ a3)) & 0xff;
            state[i + 3] = (a3 ^ t ^ xtime(a3 ^ u)) & 0xff;
        }
    }

    function invMixColumns(state) {
        for (let c = 0; c < 4; c++) {
            const i = c * 4;
            const a0 = state[i], a1 = state[i + 1], a2 = state[i + 2], a3 = state[i + 3];
            state[i] = (gmul(a0, 0x0e) ^ gmul(a1, 0x0b) ^ gmul(a2, 0x0d) ^ gmul(a3, 0x09)) & 0xff;
            state[i + 1] = (gmul(a0, 0x09) ^ gmul(a1, 0x0e) ^ gmul(a2, 0x0b) ^ gmul(a3, 0x0d)) & 0xff;
            state[i + 2] = (gmul(a0, 0x0d) ^ gmul(a1, 0x09) ^ gmul(a2, 0x0e) ^ gmul(a3, 0x0b)) & 0xff;
            state[i + 3] = (gmul(a0, 0x0b) ^ gmul(a1, 0x0d) ^ gmul(a2, 0x09) ^ gmul(a3, 0x0e)) & 0xff;
        }
    }

    function addRoundKey(state, roundKeys, round) {
        const base = round * 16;
        for (let i = 0; i < 16; i++) state[i] ^= roundKeys[base + i];
    }

    function expandAesKey(keyBytes) {
        const key = keyBytes instanceof Uint8Array ? keyBytes : Uint8Array.from(keyBytes || []);
        const keyLen = key.length;
        const Nk = keyLen === 16 ? 4 : (keyLen === 32 ? 8 : 0);
        if (!Nk) throw new Error('AES key 长度必须为 16 或 32 字节');
        const Nr = Nk === 4 ? 10 : 14;
        const Nb = 4;
        const wLen = Nb * (Nr + 1);
        const w = new Uint32Array(wLen);

        // 读取初始 key（大端 32-bit word）
        for (let i = 0; i < Nk; i++) {
            const b0 = key[i * 4];
            const b1 = key[i * 4 + 1];
            const b2 = key[i * 4 + 2];
            const b3 = key[i * 4 + 3];
            w[i] = ((b0 << 24) | (b1 << 16) | (b2 << 8) | b3) >>> 0;
        }

        function rotWord(word) {
            return ((word << 8) | (word >>> 24)) >>> 0;
        }

        function subWord(word) {
            return (
                (AES_SBOX[(word >>> 24) & 0xff] << 24) |
                (AES_SBOX[(word >>> 16) & 0xff] << 16) |
                (AES_SBOX[(word >>> 8) & 0xff] << 8) |
                (AES_SBOX[word & 0xff])
            ) >>> 0;
        }

        for (let i = Nk; i < wLen; i++) {
            let temp = w[i - 1];
            if (i % Nk === 0) {
                temp = (subWord(rotWord(temp)) ^ (AES_RCON[i / Nk] << 24)) >>> 0;
            } else if (Nk === 8 && i % Nk === 4) {
                temp = subWord(temp);
            }
            w[i] = (w[i - Nk] ^ temp) >>> 0;
        }

        // 展开为 roundKeys（字节）
        const roundKeys = new Uint8Array((Nr + 1) * 16);
        for (let i = 0; i < wLen; i++) {
            const word = w[i];
            roundKeys[i * 4] = (word >>> 24) & 0xff;
            roundKeys[i * 4 + 1] = (word >>> 16) & 0xff;
            roundKeys[i * 4 + 2] = (word >>> 8) & 0xff;
            roundKeys[i * 4 + 3] = word & 0xff;
        }
        return { roundKeys, Nr };
    }

    function aesEncryptBlock(block16, expanded) {
        const state = Uint8Array.from(block16);
        addRoundKey(state, expanded.roundKeys, 0);
        for (let r = 1; r < expanded.Nr; r++) {
            subBytes(state);
            shiftRows(state);
            mixColumns(state);
            addRoundKey(state, expanded.roundKeys, r);
        }
        subBytes(state);
        shiftRows(state);
        addRoundKey(state, expanded.roundKeys, expanded.Nr);
        return state;
    }

    function aesDecryptBlock(block16, expanded) {
        const state = Uint8Array.from(block16);
        addRoundKey(state, expanded.roundKeys, expanded.Nr);
        for (let r = expanded.Nr - 1; r >= 1; r--) {
            invShiftRows(state);
            invSubBytes(state);
            addRoundKey(state, expanded.roundKeys, r);
            invMixColumns(state);
        }
        invShiftRows(state);
        invSubBytes(state);
        addRoundKey(state, expanded.roundKeys, 0);
        return state;
    }

    function aesEcbEncrypt(plaintextBytes, keyBytes) {
        const expanded = expandAesKey(keyBytes);
        const padded = pkcs7Pad(plaintextBytes, 16);
        const out = new Uint8Array(padded.length);
        for (let i = 0; i < padded.length; i += 16) {
            out.set(aesEncryptBlock(padded.slice(i, i + 16), expanded), i);
        }
        return out;
    }

    function aesEcbDecrypt(cipherBytes, keyBytes) {
        const expanded = expandAesKey(keyBytes);
        const u8 = cipherBytes instanceof Uint8Array ? cipherBytes : Uint8Array.from(cipherBytes || []);
        if (u8.length === 0 || u8.length % 16 !== 0) throw new Error('非法密文长度（AES 块大小为 16 字节）');
        const out = new Uint8Array(u8.length);
        for (let i = 0; i < u8.length; i += 16) {
            out.set(aesDecryptBlock(u8.slice(i, i + 16), expanded), i);
        }
        return pkcs7Unpad(out, 16);
    }

    // ==================== DES（ECB） ====================
    // 使用 BigInt 实现 64-bit 块/置换，避免 32-bit 限制
    const DES_IP = [
        58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4,
        62, 54, 46, 38, 30, 22, 14, 6, 64, 56, 48, 40, 32, 24, 16, 8,
        57, 49, 41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27, 19, 11, 3,
        61, 53, 45, 37, 29, 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7
    ];
    const DES_FP = [
        40, 8, 48, 16, 56, 24, 64, 32, 39, 7, 47, 15, 55, 23, 63, 31,
        38, 6, 46, 14, 54, 22, 62, 30, 37, 5, 45, 13, 53, 21, 61, 29,
        36, 4, 44, 12, 52, 20, 60, 28, 35, 3, 43, 11, 51, 19, 59, 27,
        34, 2, 42, 10, 50, 18, 58, 26, 33, 1, 41, 9, 49, 17, 57, 25
    ];
    const DES_E = [
        32, 1, 2, 3, 4, 5, 4, 5, 6, 7, 8, 9, 8, 9, 10, 11, 12, 13,
        12, 13, 14, 15, 16, 17, 16, 17, 18, 19, 20, 21, 20, 21, 22, 23,
        24, 25, 24, 25, 26, 27, 28, 29, 28, 29, 30, 31, 32, 1
    ];
    const DES_P = [
        16, 7, 20, 21, 29, 12, 28, 17,
        1, 15, 23, 26, 5, 18, 31, 10,
        2, 8, 24, 14, 32, 27, 3, 9,
        19, 13, 30, 6, 22, 11, 4, 25
    ];
    const DES_PC1 = [
        57, 49, 41, 33, 25, 17, 9,
        1, 58, 50, 42, 34, 26, 18,
        10, 2, 59, 51, 43, 35, 27,
        19, 11, 3, 60, 52, 44, 36,
        63, 55, 47, 39, 31, 23, 15,
        7, 62, 54, 46, 38, 30, 22,
        14, 6, 61, 53, 45, 37, 29,
        21, 13, 5, 28, 20, 12, 4
    ];
    const DES_PC2 = [
        14, 17, 11, 24, 1, 5, 3, 28,
        15, 6, 21, 10, 23, 19, 12, 4,
        26, 8, 16, 7, 27, 20, 13, 2,
        41, 52, 31, 37, 47, 55, 30, 40,
        51, 45, 33, 48, 44, 49, 39, 56,
        34, 53, 46, 42, 50, 36, 29, 32
    ];
    const DES_SHIFTS = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1];
    const DES_SBOX = [
        [
            [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
            [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
            [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
            [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
        ],
        [
            [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
            [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
            [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
            [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
        ],
        [
            [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
            [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
            [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
            [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]
        ],
        [
            [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
            [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
            [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
            [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]
        ],
        [
            [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
            [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
            [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
            [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
        ],
        [
            [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
            [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
            [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
            [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
        ],
        [
            [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
            [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
            [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
            [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
        ],
        [
            [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
            [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
            [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
            [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
        ]
    ];

    function bytesToBigIntBE(bytes) {
        const u8 = bytes instanceof Uint8Array ? bytes : Uint8Array.from(bytes || []);
        let v = 0n;
        for (let i = 0; i < u8.length; i++) v = (v << 8n) | BigInt(u8[i] & 0xff);
        return v;
    }

    function bigIntToBytesBE(value, size) {
        const out = new Uint8Array(size);
        let v = BigInt(value);
        for (let i = size - 1; i >= 0; i--) {
            out[i] = Number(v & 0xffn);
            v >>= 8n;
        }
        return out;
    }

    function permuteBits(value, table, inputBits) {
        let out = 0n;
        const inBits = BigInt(inputBits);
        for (let i = 0; i < table.length; i++) {
            const pos = BigInt(table[i]);
            const bit = (BigInt(value) >> (inBits - pos)) & 1n;
            out = (out << 1n) | bit;
        }
        return out;
    }

    function rotl28(v, shift) {
        const mask = (1n << 28n) - 1n;
        const s = BigInt(shift);
        return (((v << s) & mask) | (v >> (28n - s))) & mask;
    }

    function desCreateSubKeys(key64) {
        const pc1 = permuteBits(key64, DES_PC1, 64); // 56-bit
        let c = (pc1 >> 28n) & ((1n << 28n) - 1n);
        let d = pc1 & ((1n << 28n) - 1n);
        const subKeys = [];
        for (let i = 0; i < 16; i++) {
            c = rotl28(c, DES_SHIFTS[i]);
            d = rotl28(d, DES_SHIFTS[i]);
            const cd = (c << 28n) | d;
            subKeys.push(permuteBits(cd, DES_PC2, 56)); // 48-bit
        }
        return subKeys;
    }

    function desFeistel(r32, subKey48) {
        const e48 = permuteBits(r32, DES_E, 32);
        const x = e48 ^ subKey48;

        let sOut = 0n; // 32-bit
        for (let i = 0; i < 8; i++) {
            const shift = BigInt((7 - i) * 6);
            const chunk = Number((x >> shift) & 0x3fn);
            const row = ((chunk & 0x20) >> 4) | (chunk & 0x01);
            const col = (chunk >> 1) & 0x0f;
            const val = DES_SBOX[i][row][col] & 0x0f;
            sOut = (sOut << 4n) | BigInt(val);
        }
        return permuteBits(sOut, DES_P, 32);
    }

    function desCryptBlock(block64, subKeys, decrypt) {
        const ip = permuteBits(block64, DES_IP, 64);
        let l = (ip >> 32n) & 0xffffffffn;
        let r = ip & 0xffffffffn;

        for (let i = 0; i < 16; i++) {
            const k = decrypt ? subKeys[15 - i] : subKeys[i];
            const f = desFeistel(r, k);
            const newL = r;
            const newR = (l ^ f) & 0xffffffffn;
            l = newL;
            r = newR;
        }

        const preOut = (r << 32n) | l; // swap
        return permuteBits(preOut, DES_FP, 64);
    }

    function desEcbEncrypt(plaintextBytes, keyBytes8) {
        const key = keyBytes8 instanceof Uint8Array ? keyBytes8 : Uint8Array.from(keyBytes8 || []);
        if (key.length !== 8) throw new Error('DES key 长度必须为 8 字节');
        const key64 = bytesToBigIntBE(key);
        const subKeys = desCreateSubKeys(key64);

        const padded = pkcs7Pad(plaintextBytes, 8);
        const out = new Uint8Array(padded.length);
        for (let i = 0; i < padded.length; i += 8) {
            const block = bytesToBigIntBE(padded.slice(i, i + 8));
            const enc = desCryptBlock(block, subKeys, false);
            out.set(bigIntToBytesBE(enc, 8), i);
        }
        return out;
    }

    function desEcbDecrypt(cipherBytes, keyBytes8) {
        const key = keyBytes8 instanceof Uint8Array ? keyBytes8 : Uint8Array.from(keyBytes8 || []);
        if (key.length !== 8) throw new Error('DES key 长度必须为 8 字节');
        const u8 = cipherBytes instanceof Uint8Array ? cipherBytes : Uint8Array.from(cipherBytes || []);
        if (u8.length === 0 || u8.length % 8 !== 0) throw new Error('非法密文长度（DES 块大小为 8 字节）');
        const key64 = bytesToBigIntBE(key);
        const subKeys = desCreateSubKeys(key64);

        const out = new Uint8Array(u8.length);
        for (let i = 0; i < u8.length; i += 8) {
            const block = bytesToBigIntBE(u8.slice(i, i + 8));
            const dec = desCryptBlock(block, subKeys, true);
            out.set(bigIntToBytesBE(dec, 8), i);
        }
        return pkcs7Unpad(out, 8);
    }

    return {
        utf8ToBytes,
        bytesToUtf8,
        bytesToHex,
        hexToBytes,
        base64EncodeBytes,
        base64DecodeToBytes,
        pkcs7Pad,
        pkcs7Unpad,
        adjustKeyUtf8,
        aesEcbEncrypt,
        aesEcbDecrypt,
        desEcbEncrypt,
        desEcbDecrypt
    };
});

