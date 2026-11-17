import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def create_codearena_icon(output_path="icon.png"):
    size = (1024, 1024)
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Coordinates for macOS standard squircle
    margin = 48
    rect = [margin, margin, size[0] - margin, size[1] - margin]
    radius = 210

    # Draw subtle ambient drop shadow
    shadow_img = Image.new("RGBA", size, (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow_img)
    shadow_draw.rounded_rectangle([margin, margin + 20, size[0] - margin, size[1] - margin + 20], radius=radius, fill=(0, 0, 0, 160))
    shadow_img = shadow_img.filter(ImageFilter.GaussianBlur(24))
    img = Image.alpha_composite(shadow_img, img)
    draw = ImageDraw.Draw(img)

    # Base squircle card with vertical gradient
    card = Image.new("RGBA", size, (0, 0, 0, 0))
    card_draw = ImageDraw.Draw(card)
    card_draw.rounded_rectangle(rect, radius=radius, fill=(24, 24, 28, 255))

    # Add gradient overlay
    for y in range(rect[1], rect[3]):
        ratio = (y - rect[1]) / (rect[3] - rect[1])
        # From #23232a to #0e0e12
        r = int(35 * (1 - ratio) + 14 * ratio)
        g = int(35 * (1 - ratio) + 14 * ratio)
        b = int(42 * (1 - ratio) + 18 * ratio)
        # horizontal slice within mask
        pass

    # Draw gradient directly onto card mask
    grad = Image.new("RGBA", size, (0, 0, 0, 0))
    grad_draw = ImageDraw.Draw(grad)
    for y in range(size[1]):
        ratio = y / size[1]
        r = int(38 * (1 - ratio) + 12 * ratio)
        g = int(38 * (1 - ratio) + 12 * ratio)
        b = int(46 * (1 - ratio) + 16 * ratio)
        grad_draw.line([(0, y), (size[0], y)], fill=(r, g, b, 255))

    mask = Image.new("L", size, 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle(rect, radius=radius, fill=255)
    
    img = Image.composite(grad, img, mask)
    draw = ImageDraw.Draw(img)

    # Glowing border
    draw.rounded_rectangle(rect, radius=radius, outline=(255, 161, 22, 220), width=10)
    # Inner border highlight
    inner_rect = [rect[0] + 10, rect[1] + 10, rect[2] - 10, rect[3] - 10]
    draw.rounded_rectangle(inner_rect, radius=radius - 8, outline=(255, 255, 255, 25), width=2)

    # Window titlebar dots
    dot_y = margin + 80
    dot_r = 18
    # Close
    draw.ellipse([margin + 80 - dot_r, dot_y - dot_r, margin + 80 + dot_r, dot_y + dot_r], fill=(255, 95, 86, 255))
    # Minimize
    draw.ellipse([margin + 135 - dot_r, dot_y - dot_r, margin + 135 + dot_r, dot_y + dot_r], fill=(255, 189, 46, 255))
    # Maximize / Zoom
    draw.ellipse([margin + 190 - dot_r, dot_y - dot_r, margin + 190 + dot_r, dot_y + dot_r], fill=(39, 201, 63, 255))

    # Server Status Pill in top right
    pill_w = 170
    pill_h = 44
    pill_x2 = rect[2] - 70
    pill_x1 = pill_x2 - pill_w
    pill_y1 = dot_y - pill_h // 2
    pill_y2 = dot_y + pill_h // 2
    draw.rounded_rectangle([pill_x1, pill_y1, pill_x2, pill_y2], radius=22, fill=(35, 42, 38, 220), outline=(0, 230, 118, 120), width=2)
    # Status green dot
    sdot_r = 8
    draw.ellipse([pill_x1 + 22 - sdot_r, dot_y - sdot_r, pill_x1 + 22 + sdot_r, dot_y + sdot_r], fill=(0, 230, 118, 255))

    try:
        font_status = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 22)
    except:
        font_status = ImageFont.load_default()
    draw.text((pill_x1 + 42, dot_y - 12), "SERVER", font=font_status, fill=(0, 230, 118, 255))

    # Divider bar
    div_y = margin + 140
    draw.line([(rect[0] + 40, div_y), (rect[2] - 40, div_y)], fill=(255, 255, 255, 20), width=2)

    # Big Center Visual: Code Terminal Prompt (>_)
    # Let's draw sharp stylized polygon prompt: ">" in LeetCode Orange
    # Point 1 (top left), Point 2 (middle right), Point 3 (bottom left)
    prompt_top_y = 360
    prompt_mid_y = 512
    prompt_bot_y = 664
    
    p_x1 = 260
    p_x2 = 410
    thickness = 58

    # Outer chevron
    chevron_pts = [
        (p_x1, prompt_top_y),
        (p_x2, prompt_mid_y),
        (p_x1, prompt_bot_y),
        (p_x1 + thickness, prompt_bot_y),
        (p_x2 + thickness, prompt_mid_y),
        (p_x1 + thickness, prompt_top_y)
    ]
    draw.polygon(chevron_pts, fill=(255, 161, 22, 255))

    # Terminal cursor "_"
    cur_x1 = 510
    cur_x2 = 740
    cur_y1 = prompt_bot_y - 48
    cur_y2 = prompt_bot_y + 10
    draw.rounded_rectangle([cur_x1, cur_y1, cur_x2, cur_y2], radius=8, fill=(255, 255, 255, 240))

    # Subtle inner code brackets behind/accent
    try:
        font_code = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 60)
        draw.text((510, 375), "PORT: 8080", font=font_code, fill=(140, 145, 160, 200))
        draw.text((510, 445), "MySQL • C++", font=font_code, fill=(255, 161, 22, 190))
    except Exception as e:
        pass

    # Brand Title at the bottom
    try:
        font_brand = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 58)
        bbox = draw.textbbox((0, 0), "CODEARENA", font=font_brand)
        w = bbox[2] - bbox[0]
        brand_x = (size[0] - w) // 2
        draw.text((brand_x, 810), "CODEARENA", font=font_brand, fill=(240, 242, 248, 255))
    except Exception as e:
        pass

    # Subtitle: LOCAL ENVIRONMENT
    try:
        font_sub = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
        bbox_sub = draw.textbbox((0, 0), "LEETCODE PRACTICE ENGINE", font=font_sub)
        w_sub = bbox_sub[2] - bbox_sub[0]
        sub_x = (size[0] - w_sub) // 2
        draw.text((sub_x, 880), "LEETCODE PRACTICE ENGINE", font=font_sub, fill=(255, 161, 22, 230))
    except Exception as e:
        pass

    img.save(output_path, "PNG")
    print(f"Generated icon at {output_path}")

if __name__ == "__main__":
    create_codearena_icon("icon.png")
