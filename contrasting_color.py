import colorsys

class ContrastingComplementaryColor:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "r": ("INT", {"default": 14, "min": 0, "max": 255}),
                "g": ("INT", {"default": 21, "min": 0, "max": 255}),
                "b": ("INT", {"default": 19, "min": 0, "max": 255}),
                "threshold": ("FLOAT", {"default": 0.5, "min": 0.0, "max": 1.0}),
                "dark_value": ("FLOAT", {"default": 0.2, "min": 0.0, "max": 1.0}),
                "bright_value": ("FLOAT", {"default": 0.85, "min": 0.0, "max": 1.0}),
                "saturation": ("FLOAT", {"default": 0.9, "min": 0.0, "max": 1.0}),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "compute_color"
    CATEGORY = "utils"
    OUTPUT_NODE = True

    # Relative luminance helper (assuming sRGB/Rec.709).
    def relative_luminance(self, r, g, b):
        def channel_lin(c):
            c_f = c / 255
            return c_f / 12.92 if c_f <= 0.03928 else ((c_f + 0.055) / 1.055) ** 2.4

        R = channel_lin(r)
        G = channel_lin(g)
        B = channel_lin(b)
        return 0.2126 * R + 0.7152 * G + 0.0722 * B

    def rgb_to_hex(self, r, g, b):
        return f"#{r:02X}{g:02X}{b:02X}"

    def compute_color(self, r, g, b, threshold=0.5, dark_value=0.2, bright_value=0.85, saturation=0.9):
        """
        1) Compute relative luminance of input color (r,g,b).
        2) Shift hue by 180 degrees (complement).
        3) If background is dark, produce a bright color. If background is light, produce a darker color.
        4) Output the final RGB as a hex string.
        """

        # 1) Luminance
        lum = self.relative_luminance(r, g, b)

        # 2) Convert input to HSV, shift hue by 0.5 (180 degrees)
        rf, gf, bf = r / 255.0, g / 255.0, b / 255.0
        h, s, v = colorsys.rgb_to_hsv(rf, gf, bf)
        h = (h + 0.5) % 1.0  # 180-degree shift

        # 3) Decide brightness based on background luminance
        #    - If background is dark (lum < threshold), we pick a bright color
        #    - If background is light (lum >= threshold), we pick a darker color
        if lum < threshold:
            # Keep saturation high, set value to bright_value
            s = saturation
            v = bright_value
        else:
            s = saturation
            v = dark_value

        # Convert back to RGB
        rr, gg, bb = colorsys.hsv_to_rgb(h, s, v)
        r_out = int(round(rr * 255))
        g_out = int(round(gg * 255))
        b_out = int(round(bb * 255))

        # 4) Return the color as a hex string
        return (self.rgb_to_hex(r_out, g_out, b_out),)



NODE_CLASS_MAPPINGS = {
    "ContrastingComplementaryColor|pysssss": ContrastingComplementaryColor

}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ContrastingComplementaryColor|pysssss": "Contrasting Complementary Color"
}

