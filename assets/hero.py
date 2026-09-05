from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math
import random
import os


# ============================================================
# CONFIGURATION
# ============================================================

WIDTH = 1400
HEIGHT = 460

FRAMES = 60
FRAME_DURATION = 70

OUTPUT = os.path.join(
    os.path.dirname(__file__),
    "hero.gif"
)


# ============================================================
# COLORS
# ============================================================

BACKGROUND = (7, 7, 10)

GRID = (24, 23, 30)

WHITE = (238, 236, 232)

MUTED = (150, 147, 155)

VIOLET = (150, 105, 210)

VIOLET_BRIGHT = (190, 145, 245)

DIM_VIOLET = (85, 62, 105)


# ============================================================
# FONTS
# ============================================================

FONT_BOLD = r"C:\Windows\Fonts\arialbd.ttf"
FONT_MONO = r"C:\Windows\Fonts\consola.ttf"


def get_font(path, size):

    try:
        return ImageFont.truetype(path, size)

    except OSError:

        return ImageFont.truetype(
            r"C:\Windows\Fonts\arial.ttf",
            size
        )


# ============================================================
# PARTICLES
# ============================================================

random.seed(42)

particles = []

for _ in range(90):

    particles.append({
        "x": random.randint(0, WIDTH),
        "y": random.randint(0, HEIGHT),
        "size": random.choice([1, 1, 1, 2]),
        "phase": random.random() * math.pi * 2
    })


# ============================================================
# NETWORK
# ============================================================

CENTER_X = 1080
CENTER_Y = 230

NODE_COUNT = 9

nodes = []

for i in range(NODE_COUNT):

    angle = (2 * math.pi / NODE_COUNT) * i

    radius = random.choice([
        70,
        105,
        135
    ])

    nodes.append({
        "angle": angle,
        "radius": radius,
        "speed": random.choice([
            0.006,
            0.008,
            0.010
        ])
    })


# ============================================================
# CREATE FRAME
# ============================================================

def create_frame(frame_number):

    image = Image.new(
        "RGBA",
        (WIDTH, HEIGHT),
        (*BACKGROUND, 255)
    )

    draw = ImageDraw.Draw(image)


    # ========================================================
    # SUBTLE BACKGROUND GRID
    # ========================================================

    for x in range(0, WIDTH, 70):

        draw.line(
            (x, 0, x, HEIGHT),
            fill=(*GRID, 55),
            width=1
        )

    for y in range(0, HEIGHT, 70):

        draw.line(
            (0, y, WIDTH, y),
            fill=(*GRID, 55),
            width=1
        )


    # ========================================================
    # BACKGROUND PARTICLES
    # ========================================================

    for particle in particles:

        alpha = int(
            25
            + 25 * (
                0.5
                + 0.5 * math.sin(
                    frame_number * 0.08
                    + particle["phase"]
                )
            )
        )

        r = particle["size"]

        draw.ellipse(
            (
                particle["x"] - r,
                particle["y"] - r,
                particle["x"] + r,
                particle["y"] + r
            ),
            fill=(
                VIOLET[0],
                VIOLET[1],
                VIOLET[2],
                alpha
            )
        )


    # ========================================================
    # NAME
    # ========================================================

    name_font = get_font(
        FONT_BOLD,
        58
    )

    name = "MONALISA MAJUMDER"

    # Calculate width so the name can be centered
    bbox = draw.textbbox(
        (0, 0),
        name,
        font=name_font
    )

    name_width = bbox[2] - bbox[0]

    name_x = (
        350 - name_width / 2
    )

    draw.text(
        (name_x, 135),
        name,
        font=name_font,
        fill=(*WHITE, 255)
    )


    # ========================================================
    # ACCENT LINE
    # ========================================================

    draw.line(
        (110, 215, 590, 215),
        fill=(*VIOLET, 210),
        width=2
    )


    # ========================================================
    # PROFESSIONAL TITLE
    # ========================================================

    title = (
        "AI / ML ENGINEER   •   "
        "INTELLIGENT SYSTEMS   •   BUILDER"
    )

    title_font = get_font(
        FONT_MONO,
        17
    )

    bbox = draw.textbbox(
        (0, 0),
        title,
        font=title_font
    )

    title_width = bbox[2] - bbox[0]

    title_x = (
        350 - title_width / 2
    )

    draw.text(
        (title_x, 250),
        title,
        font=title_font,
        fill=(*WHITE, 240)
    )


    # ========================================================
    # SHORT TAGLINE
    # ========================================================

    tagline = (
        "building  →  experimenting  →  learning"
    )

    tagline_font = get_font(
        FONT_MONO,
        16
    )

    bbox = draw.textbbox(
        (0, 0),
        tagline,
        font=tagline_font
    )

    tagline_width = bbox[2] - bbox[0]

    tagline_x = (
        350 - tagline_width / 2
    )

    draw.text(
        (tagline_x, 290),
        tagline,
        font=tagline_font,
        fill=(*MUTED, 230)
    )


    # ========================================================
    # NETWORK LAYER
    # ========================================================

    network_layer = Image.new(
        "RGBA",
        (WIDTH, HEIGHT),
        (0, 0, 0, 0)
    )

    network = ImageDraw.Draw(
        network_layer
    )


    # ========================================================
    # CALCULATE NODE POSITIONS
    # ========================================================

    calculated_nodes = []

    for node in nodes:

        angle = (
            node["angle"]
            + frame_number * node["speed"]
        )

        radius = node["radius"]

        x = (
            CENTER_X
            + math.cos(angle) * radius
        )

        y = (
            CENTER_Y
            + math.sin(angle)
            * radius
            * 0.68
        )

        calculated_nodes.append(
            (x, y)
        )


    # ========================================================
    # ORBIT RINGS
    # ========================================================

    for radius in [
        65,
        105,
        145
    ]:

        network.ellipse(
            (
                CENTER_X - radius,
                CENTER_Y - radius * 0.68,
                CENTER_X + radius,
                CENTER_Y + radius * 0.68
            ),
            outline=(
                *DIM_VIOLET,
                100
            ),
            width=1
        )


    # ========================================================
    # CONNECTIONS
    # ========================================================

    for i in range(
        len(calculated_nodes)
    ):

        for j in range(
            i + 1,
            len(calculated_nodes)
        ):

            x1, y1 = calculated_nodes[i]

            x2, y2 = calculated_nodes[j]

            distance = math.hypot(
                x2 - x1,
                y2 - y1
            )

            if distance < 105:

                network.line(
                    (
                        x1,
                        y1,
                        x2,
                        y2
                    ),
                    fill=(
                        *VIOLET,
                        105
                    ),
                    width=1
                )


    # ========================================================
    # MOVING DATA PARTICLES
    # ========================================================

    for i in range(
        len(calculated_nodes)
    ):

        start = calculated_nodes[i]

        end = calculated_nodes[
            (i + 2)
            % len(calculated_nodes)
        ]

        progress = (
            frame_number * 0.018
            + i * 0.17
        ) % 1.0

        x = (
            start[0]
            + (
                end[0]
                - start[0]
            )
            * progress
        )

        y = (
            start[1]
            + (
                end[1]
                - start[1]
            )
            * progress
        )

        network.ellipse(
            (
                x - 3,
                y - 3,
                x + 3,
                y + 3
            ),
            fill=(
                *VIOLET_BRIGHT,
                230
            )
        )


    # ========================================================
    # NETWORK NODES
    # ========================================================

    for x, y in calculated_nodes:

        network.ellipse(
            (
                x - 5,
                y - 5,
                x + 5,
                y + 5
            ),
            fill=(
                *WHITE,
                245
            )
        )

        network.ellipse(
            (
                x - 2,
                y - 2,
                x + 2,
                y + 2
            ),
            fill=(
                *VIOLET_BRIGHT,
                255
            )
        )


    # ========================================================
    # CENTRAL CORE GLOW
    # ========================================================

    glow = Image.new(
        "RGBA",
        (WIDTH, HEIGHT),
        (0, 0, 0, 0)
    )

    glow_draw = ImageDraw.Draw(
        glow
    )

    pulse = (
        1
        + 0.18
        * math.sin(
            frame_number * 0.18
        )
    )

    for radius, alpha in [
        (55, 15),
        (40, 25),
        (28, 45)
    ]:

        r = radius * pulse

        glow_draw.ellipse(
            (
                CENTER_X - r,
                CENTER_Y - r,
                CENTER_X + r,
                CENTER_Y + r
            ),
            fill=(
                VIOLET[0],
                VIOLET[1],
                VIOLET[2],
                alpha
            )
        )

    glow = glow.filter(
        ImageFilter.GaussianBlur(12)
    )


    # Add glow
    image = Image.alpha_composite(
        image,
        glow
    )


    # Add network
    image = Image.alpha_composite(
        image,
        network_layer
    )


    draw = ImageDraw.Draw(
        image
    )


    # ========================================================
    # CENTRAL CORE
    # ========================================================

    draw.ellipse(
        (
            CENTER_X - 15,
            CENTER_Y - 15,
            CENTER_X + 15,
            CENTER_Y + 15
        ),
        fill=(
            *BACKGROUND,
            255
        ),
        outline=(
            *VIOLET_BRIGHT,
            255
        ),
        width=2
    )

    draw.ellipse(
        (
            CENTER_X - 5,
            CENTER_Y - 5,
            CENTER_X + 5,
            CENTER_Y + 5
        ),
        fill=(
            *WHITE,
            255
        )
    )




    # ========================================================
    # VERY SUBTLE BOTTOM LINE
    # ========================================================

    draw.line(
        (
            110,
            390,
            WIDTH - 110,
            390
        ),
        fill=(
            *DIM_VIOLET,
            100
        ),
        width=1
    )


    return image


# ============================================================
# GENERATE ANIMATION
# ============================================================

print(
    "Generating futuristic profile animation..."
)

frames = []

for frame_number in range(
    FRAMES
):

    frame = create_frame(
        frame_number
    )

    frame = frame.convert(
        "P",
        palette=Image.Palette.ADAPTIVE,
        colors=128
    )

    frames.append(
        frame
    )

    print(
        f"\rFrame "
        f"{frame_number + 1}"
        f"/{FRAMES}",
        end=""
    )


print()

frames[0].save(
    OUTPUT,
    save_all=True,
    append_images=frames[1:],
    duration=FRAME_DURATION,
    loop=0,
    optimize=True
)

print()
print(
    "✓ Animation generated successfully!"
)

print(
    f"✓ Output: {OUTPUT}"
)