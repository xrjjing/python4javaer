/* 工具箱（M7）通用算法工具：Base64 ↔ Hex 互转
 *
 * 设计目标：
 * - 纯算法、无 DOM 依赖，便于浏览器与 Node 环境复用与单元测试
 * - 支持输入中包含空白字符（自动忽略）
 * - Hex 输出统一为小写
 */
(function (root, factory) {
    if (typeof module !== 'undefined' && module.exports) {
        module.exports = factory();
    } else {
        root.DogToolboxM7Utils = factory();
    }
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
    'use strict';

    function isNodeEnv() {
        return typeof process !== 'undefined' && process.versions && process.versions.node;
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

    function base64ToHex(b64) {
        return bytesToHex(base64DecodeToBytes(b64));
    }

    function hexToBase64(hex) {
        return base64EncodeBytes(hexToBytes(hex));
    }

    return {
        bytesToHex,
        hexToBytes,
        base64EncodeBytes,
        base64DecodeToBytes,
        base64ToHex,
        hexToBase64
    };
});

