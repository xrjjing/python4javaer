/* 工具箱（M14）颜色转换器
 *
 * 设计目标：
 * - 纯算法、无 DOM 依赖
 * - 支持 HEX、RGB、HSL 等格式互转
 * - 支持透明度（Alpha）
 */
(function (root, factory) {
    if (typeof module !== 'undefined' && module.exports) {
        module.exports = factory();
    } else {
        root.DogToolboxM14Utils = factory();
    }
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
    'use strict';

    /**
     * 解析颜色字符串，返回统一的 RGBA 对象
     * @param {string} input - 颜色字符串
     * @returns {{r: number, g: number, b: number, a: number, format: string, error?: string}}
     */
    function parseColor(input) {
        if (!input || typeof input !== 'string') {
            return { r: 0, g: 0, b: 0, a: 1, format: 'unknown', error: '无效输入' };
        }

        const str = input.trim().toLowerCase();

        // HEX 格式: #RGB, #RGBA, #RRGGBB, #RRGGBBAA
        if (str.startsWith('#')) {
            return parseHex(str);
        }

        // RGB/RGBA 格式
        if (str.startsWith('rgb')) {
            return parseRgb(str);
        }

        // HSL/HSLA 格式
        if (str.startsWith('hsl')) {
            return parseHsl(str);
        }

        // 尝试作为纯 HEX（无 # 前缀）
        if (/^[0-9a-f]{3,8}$/i.test(str)) {
            return parseHex('#' + str);
        }

        return { r: 0, g: 0, b: 0, a: 1, format: 'unknown', error: '无法识别的颜色格式' };
    }

    /**
     * 解析 HEX 颜色
     */
    function parseHex(hex) {
        const h = hex.replace('#', '');
        let r, g, b, a = 1;

        if (h.length === 3) {
            // #RGB
            r = parseInt(h[0] + h[0], 16);
            g = parseInt(h[1] + h[1], 16);
            b = parseInt(h[2] + h[2], 16);
        } else if (h.length === 4) {
            // #RGBA
            r = parseInt(h[0] + h[0], 16);
            g = parseInt(h[1] + h[1], 16);
            b = parseInt(h[2] + h[2], 16);
            a = parseInt(h[3] + h[3], 16) / 255;
        } else if (h.length === 6) {
            // #RRGGBB
            r = parseInt(h.slice(0, 2), 16);
            g = parseInt(h.slice(2, 4), 16);
            b = parseInt(h.slice(4, 6), 16);
        } else if (h.length === 8) {
            // #RRGGBBAA
            r = parseInt(h.slice(0, 2), 16);
            g = parseInt(h.slice(2, 4), 16);
            b = parseInt(h.slice(4, 6), 16);
            a = parseInt(h.slice(6, 8), 16) / 255;
        } else {
            return { r: 0, g: 0, b: 0, a: 1, format: 'hex', error: '无效的 HEX 格式' };
        }

        if (isNaN(r) || isNaN(g) || isNaN(b) || isNaN(a)) {
            return { r: 0, g: 0, b: 0, a: 1, format: 'hex', error: '无效的 HEX 值' };
        }

        return { r, g, b, a, format: 'hex' };
    }

    /**
     * 解析 RGB/RGBA 颜色
     */
    function parseRgb(str) {
        // rgb(255, 128, 0) 或 rgba(255, 128, 0, 0.5) 或现代语法 rgb(255 128 0 / 50%)
        const match = str.match(/rgba?\s*\(\s*(\d+\.?\d*%?)\s*[,\s]\s*(\d+\.?\d*%?)\s*[,\s]\s*(\d+\.?\d*%?)\s*(?:[,\/]\s*(\d*\.?\d+%?))?\s*\)/);

        if (!match) {
            return { r: 0, g: 0, b: 0, a: 1, format: 'rgb', error: '无效的 RGB 格式' };
        }

        let r = parseColorValue(match[1], 255);
        let g = parseColorValue(match[2], 255);
        let b = parseColorValue(match[3], 255);
        let a = match[4] !== undefined ? parseColorValue(match[4], 1) : 1;

        r = clamp(Math.round(r), 0, 255);
        g = clamp(Math.round(g), 0, 255);
        b = clamp(Math.round(b), 0, 255);
        a = clamp(a, 0, 1);

        return { r, g, b, a, format: match[4] !== undefined ? 'rgba' : 'rgb' };
    }

    /**
     * 解析 HSL/HSLA 颜色
     */
    function parseHsl(str) {
        // hsl(120, 50%, 50%) 或 hsla(120, 50%, 50%, 0.5) 或现代语法 hsl(120 50% 50% / 50%)
        const match = str.match(/hsla?\s*\(\s*(\d+\.?\d*)\s*[,\s]\s*(\d+\.?\d*)%?\s*[,\s]\s*(\d+\.?\d*)%?\s*(?:[,\/]\s*(\d*\.?\d+%?))?\s*\)/);

        if (!match) {
            return { r: 0, g: 0, b: 0, a: 1, format: 'hsl', error: '无效的 HSL 格式' };
        }

        let h = parseFloat(match[1]) % 360;
        let s = parseFloat(match[2]) / 100;
        let l = parseFloat(match[3]) / 100;
        let a = match[4] !== undefined ? parseColorValue(match[4], 1) : 1;

        if (h < 0) h += 360;
        s = clamp(s, 0, 1);
        l = clamp(l, 0, 1);
        a = clamp(a, 0, 1);

        const { r, g, b } = hslToRgb(h, s, l);

        return { r, g, b, a, format: match[4] !== undefined ? 'hsla' : 'hsl' };
    }

    /**
     * 解析颜色值（支持百分比）
     */
    function parseColorValue(val, max) {
        if (typeof val === 'string' && val.endsWith('%')) {
            return (parseFloat(val) / 100) * max;
        }
        return parseFloat(val);
    }

    /**
     * HSL 转 RGB
     */
    function hslToRgb(h, s, l) {
        let r, g, b;

        if (s === 0) {
            r = g = b = l;
        } else {
            const q = l < 0.5 ? l * (1 + s) : l + s - l * s;
            const p = 2 * l - q;
            r = hueToRgb(p, q, h / 360 + 1/3);
            g = hueToRgb(p, q, h / 360);
            b = hueToRgb(p, q, h / 360 - 1/3);
        }

        return {
            r: Math.round(r * 255),
            g: Math.round(g * 255),
            b: Math.round(b * 255)
        };
    }

    function hueToRgb(p, q, t) {
        if (t < 0) t += 1;
        if (t > 1) t -= 1;
        if (t < 1/6) return p + (q - p) * 6 * t;
        if (t < 1/2) return q;
        if (t < 2/3) return p + (q - p) * (2/3 - t) * 6;
        return p;
    }

    /**
     * RGB 转 HSL
     */
    function rgbToHsl(r, g, b) {
        r /= 255;
        g /= 255;
        b /= 255;

        const max = Math.max(r, g, b);
        const min = Math.min(r, g, b);
        let h, s, l = (max + min) / 2;

        if (max === min) {
            h = s = 0;
        } else {
            const d = max - min;
            s = l > 0.5 ? d / (2 - max - min) : d / (max + min);

            switch (max) {
                case r: h = ((g - b) / d + (g < b ? 6 : 0)) / 6; break;
                case g: h = ((b - r) / d + 2) / 6; break;
                case b: h = ((r - g) / d + 4) / 6; break;
            }
        }

        return {
            h: Math.round(h * 360),
            s: Math.round(s * 100),
            l: Math.round(l * 100)
        };
    }

    /**
     * RGB 转 HSV
     */
    function rgbToHsv(r, g, b) {
        r /= 255;
        g /= 255;
        b /= 255;

        const max = Math.max(r, g, b);
        const min = Math.min(r, g, b);
        let h, s, v = max;

        const d = max - min;
        s = max === 0 ? 0 : d / max;

        if (max === min) {
            h = 0;
        } else {
            switch (max) {
                case r: h = ((g - b) / d + (g < b ? 6 : 0)) / 6; break;
                case g: h = ((b - r) / d + 2) / 6; break;
                case b: h = ((r - g) / d + 4) / 6; break;
            }
        }

        return {
            h: Math.round(h * 360),
            s: Math.round(s * 100),
            v: Math.round(v * 100)
        };
    }

    /**
     * RGB 转 CMYK
     */
    function rgbToCmyk(r, g, b) {
        r /= 255;
        g /= 255;
        b /= 255;

        const k = 1 - Math.max(r, g, b);

        if (k === 1) {
            return { c: 0, m: 0, y: 0, k: 100 };
        }

        const c = (1 - r - k) / (1 - k);
        const m = (1 - g - k) / (1 - k);
        const y = (1 - b - k) / (1 - k);

        return {
            c: Math.round(c * 100),
            m: Math.round(m * 100),
            y: Math.round(y * 100),
            k: Math.round(k * 100)
        };
    }

    // ========== 格式化输出 ==========

    /**
     * 转为 HEX 格式
     */
    function toHex(color, includeAlpha = false) {
        const { r, g, b, a } = color;
        const hex = '#' +
            r.toString(16).padStart(2, '0') +
            g.toString(16).padStart(2, '0') +
            b.toString(16).padStart(2, '0');

        if (includeAlpha && a < 1) {
            return hex + Math.round(a * 255).toString(16).padStart(2, '0');
        }
        return hex.toUpperCase();
    }

    /**
     * 转为 RGB/RGBA 格式
     */
    function toRgb(color, forceAlpha = false) {
        const { r, g, b, a } = color;
        if (a < 1 || forceAlpha) {
            return `rgba(${r}, ${g}, ${b}, ${roundTo(a, 2)})`;
        }
        return `rgb(${r}, ${g}, ${b})`;
    }

    /**
     * 转为 HSL/HSLA 格式
     */
    function toHsl(color, forceAlpha = false) {
        const { r, g, b, a } = color;
        const { h, s, l } = rgbToHsl(r, g, b);
        if (a < 1 || forceAlpha) {
            return `hsla(${h}, ${s}%, ${l}%, ${roundTo(a, 2)})`;
        }
        return `hsl(${h}, ${s}%, ${l}%)`;
    }

    /**
     * 转为 HSV 格式
     */
    function toHsv(color) {
        const { r, g, b } = color;
        const { h, s, v } = rgbToHsv(r, g, b);
        return `hsv(${h}, ${s}%, ${v}%)`;
    }

    /**
     * 转为 CMYK 格式
     */
    function toCmyk(color) {
        const { r, g, b } = color;
        const { c, m, y, k } = rgbToCmyk(r, g, b);
        return `cmyk(${c}%, ${m}%, ${y}%, ${k}%)`;
    }

    /**
     * 获取所有格式
     */
    function getAllFormats(color) {
        return {
            hex: toHex(color),
            hexAlpha: toHex(color, true),
            rgb: toRgb(color),
            rgba: toRgb(color, true),
            hsl: toHsl(color),
            hsla: toHsl(color, true),
            hsv: toHsv(color),
            cmyk: toCmyk(color)
        };
    }

    // ========== 颜色操作 ==========

    /**
     * 调整亮度
     * @param {object} color - RGBA 对象
     * @param {number} amount - -100 到 100
     */
    function adjustBrightness(color, amount) {
        const { r, g, b, a } = color;
        const { h, s, l } = rgbToHsl(r, g, b);
        const newL = clamp(l + amount, 0, 100);
        const rgb = hslToRgb(h, s / 100, newL / 100);
        return { ...rgb, a };
    }

    /**
     * 调整饱和度
     */
    function adjustSaturation(color, amount) {
        const { r, g, b, a } = color;
        const { h, s, l } = rgbToHsl(r, g, b);
        const newS = clamp(s + amount, 0, 100);
        const rgb = hslToRgb(h, newS / 100, l / 100);
        return { ...rgb, a };
    }

    /**
     * 获取互补色
     */
    function getComplementary(color) {
        const { r, g, b, a } = color;
        const { h, s, l } = rgbToHsl(r, g, b);
        const newH = (h + 180) % 360;
        const rgb = hslToRgb(newH, s / 100, l / 100);
        return { ...rgb, a };
    }

    /**
     * 获取三等分色
     */
    function getTriadic(color) {
        const { r, g, b, a } = color;
        const { h, s, l } = rgbToHsl(r, g, b);
        const h1 = (h + 120) % 360;
        const h2 = (h + 240) % 360;
        return [
            { ...hslToRgb(h1, s / 100, l / 100), a },
            { ...hslToRgb(h2, s / 100, l / 100), a }
        ];
    }

    /**
     * 获取类似色
     */
    function getAnalogous(color, angle = 30) {
        const { r, g, b, a } = color;
        const { h, s, l } = rgbToHsl(r, g, b);
        const h1 = (h + angle + 360) % 360;
        const h2 = (h - angle + 360) % 360;
        return [
            { ...hslToRgb(h1, s / 100, l / 100), a },
            { ...hslToRgb(h2, s / 100, l / 100), a }
        ];
    }

    /**
     * 计算对比度（WCAG）
     */
    function getContrastRatio(color1, color2) {
        const l1 = getLuminance(color1);
        const l2 = getLuminance(color2);
        const lighter = Math.max(l1, l2);
        const darker = Math.min(l1, l2);
        return (lighter + 0.05) / (darker + 0.05);
    }

    /**
     * 获取相对亮度
     */
    function getLuminance(color) {
        const { r, g, b } = color;
        const [rs, gs, bs] = [r, g, b].map(c => {
            c /= 255;
            return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
        });
        return 0.2126 * rs + 0.7152 * gs + 0.0722 * bs;
    }

    /**
     * 判断是否为深色
     */
    function isDark(color) {
        return getLuminance(color) < 0.5;
    }

    // ========== 工具函数 ==========

    function clamp(val, min, max) {
        return Math.min(Math.max(val, min), max);
    }

    function roundTo(num, decimals) {
        const factor = Math.pow(10, decimals);
        return Math.round(num * factor) / factor;
    }

    return {
        parseColor,
        toHex,
        toRgb,
        toHsl,
        toHsv,
        toCmyk,
        getAllFormats,
        rgbToHsl,
        rgbToHsv,
        rgbToCmyk,
        hslToRgb,
        adjustBrightness,
        adjustSaturation,
        getComplementary,
        getTriadic,
        getAnalogous,
        getContrastRatio,
        getLuminance,
        isDark
    };
});
