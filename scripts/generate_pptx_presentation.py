"""
Generate simplified, presentation-ready 12-slide widescreen PowerPoint for DSA Mini Project.
Target: docs/DSA_Mini_Project_Presentation.pptx and docs/DSA_Mini_Project_Presentation.ppt
"""
import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# Widescreen 16:9 dimensions
SLIDE_WIDTH = Inches(13.333)
SLIDE_HEIGHT = Inches(7.5)

# Professional Color Palette
NAVY_DARK = RGBColor(15, 23, 42)      # #0F172A
NAVY_CARD = RGBColor(30, 41, 59)      # #1E293B
BLUE_ACCENT = RGBColor(37, 99, 235)   # #2563EB
TEAL_ACCENT = RGBColor(13, 148, 136)  # #0D9488
CYAN_ACCENT = RGBColor(6, 182, 212)   # #06B6D4
AMBER_ACCENT = RGBColor(217, 119, 6)  # #D97706
GREEN_ACCENT = RGBColor(16, 185, 129) # #10B981
BG_LIGHT = RGBColor(248, 250, 252)    # #F8FAFC
CARD_BG = RGBColor(255, 255, 255)     # #FFFFFF
CARD_BORDER = RGBColor(226, 232, 240) # #E2E8F0
TEXT_MAIN = RGBColor(30, 41, 59)      # #1E293B
TEXT_MUTED = RGBColor(100, 116, 139)  # #64748B
TEXT_WHITE = RGBColor(255, 255, 255)
TEXT_SUBTLE = RGBColor(203, 213, 225) # #CBD5E1


def create_presentation():
    prs = Presentation()
    prs.slide_width = SLIDE_WIDTH
    prs.slide_height = SLIDE_HEIGHT
    blank_layout = prs.slide_layouts[6]

    def set_slide_background(slide, color):
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = color

    def add_header(slide, title_text, category_badge="DATA STREAM ANALYTICS"):
        # Header banner
        shape_top = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), SLIDE_WIDTH, Inches(1.15)
        )
        shape_top.fill.solid()
        shape_top.fill.fore_color.rgb = NAVY_DARK
        shape_top.line.fill.background()

        # Accent underline
        line = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, Inches(0), Inches(1.15), SLIDE_WIDTH, Inches(0.05)
        )
        line.fill.solid()
        line.fill.fore_color.rgb = BLUE_ACCENT
        line.line.fill.background()

        # Category / Badge
        badge_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.12), Inches(10), Inches(0.28))
        tf_badge = badge_box.text_frame
        tf_badge.word_wrap = True
        p_badge = tf_badge.paragraphs[0]
        p_badge.text = category_badge.upper()
        p_badge.font.size = Pt(9.5)
        p_badge.font.bold = True
        p_badge.font.color.rgb = CYAN_ACCENT

        # Title text
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.38), Inches(11.5), Inches(0.65))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(21)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_WHITE

    def add_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=CARD_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1.2)
        return card

    # =========================================================================
    # SLIDE 1: TITLE, GROUP MEMBERS & SUBMITTED TO (NO ACADEMIC YEAR)
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide1, NAVY_DARK)

    accent_bar = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(0.4), SLIDE_HEIGHT)
    accent_bar.fill.solid()
    accent_bar.fill.fore_color.rgb = BLUE_ACCENT
    accent_bar.line.fill.background()

    tb_sub = slide1.shapes.add_textbox(Inches(1.2), Inches(0.55), Inches(11), Inches(0.4))
    p_sub = tb_sub.text_frame.paragraphs[0]
    p_sub.text = "DATA STREAM ANALYTICS  |  DSA MINI PROJECT"
    p_sub.font.size = Pt(13)
    p_sub.font.bold = True
    p_sub.font.color.rgb = CYAN_ACCENT

    tb_title = slide1.shapes.add_textbox(Inches(1.2), Inches(1.0), Inches(11), Inches(1.4))
    p_t1 = tb_title.text_frame.paragraphs[0]
    p_t1.text = "REAL-TIME IoT SENSOR STREAMING ANALYTICS"
    p_t1.font.size = Pt(26)
    p_t1.font.bold = True
    p_t1.font.color.rgb = TEXT_WHITE

    p_t2 = tb_title.text_frame.add_paragraph()
    p_t2.text = "AND ANOMALY DETECTION SYSTEM"
    p_t2.font.size = Pt(26)
    p_t2.font.bold = True
    p_t2.font.color.rgb = BLUE_ACCENT

    # Main Card containing Team and Faculty
    add_card(slide1, Inches(1.2), Inches(2.6), Inches(11), Inches(4.2), NAVY_CARD, RGBColor(51, 65, 85))

    tb_grp = slide1.shapes.add_textbox(Inches(1.5), Inches(2.75), Inches(10), Inches(0.35))
    p_g = tb_grp.text_frame.paragraphs[0]
    p_g.text = "GROUP NO: 3  |  GROUP MEMBERS"
    p_g.font.size = Pt(13.5)
    p_g.font.bold = True
    p_g.font.color.rgb = CYAN_ACCENT

    members = [
        ("23BTRCL227", "P CHETHAN"),
        ("23BTRCL217", "MUKKAMALLA LOKESHWAR REDDY"),
        ("23BTRCL221", "NADAKUDURU SRINIVAS"),
        ("23BTRCL233", "SOMISETTY JAGANNADA KAILASH"),
    ]
    coords = [
        (Inches(1.5), Inches(3.2)),
        (Inches(6.8), Inches(3.2)),
        (Inches(1.5), Inches(4.2)),
        (Inches(6.8), Inches(4.2)),
    ]
    for (usn, name), (mx, my) in zip(members, coords):
        m_card = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, mx, my, Inches(5.1), Inches(0.85))
        m_card.fill.solid()
        m_card.fill.fore_color.rgb = RGBColor(15, 23, 42)
        m_card.line.color.rgb = RGBColor(71, 85, 105)
        m_card.line.width = Pt(1)

        m_tb = slide1.shapes.add_textbox(mx + Inches(0.2), my + Inches(0.08), Inches(4.7), Inches(0.68))
        m_p1 = m_tb.text_frame.paragraphs[0]
        m_p1.text = f"USN: {usn}"
        m_p1.font.size = Pt(10.5)
        m_p1.font.bold = True
        m_p1.font.color.rgb = BLUE_ACCENT

        m_p2 = m_tb.text_frame.add_paragraph()
        m_p2.text = name
        m_p2.font.size = Pt(12)
        m_p2.font.bold = True
        m_p2.font.color.rgb = TEXT_WHITE

    # Submitted To Card
    sub_card = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.5), Inches(5.25), Inches(10.4), Inches(0.75))
    sub_card.fill.solid()
    sub_card.fill.fore_color.rgb = RGBColor(15, 23, 42)
    sub_card.line.color.rgb = RGBColor(71, 85, 105)
    sub_card.line.width = Pt(1)

    tb_subto = slide1.shapes.add_textbox(Inches(1.7), Inches(5.32), Inches(10.0), Inches(0.6))
    p_st = tb_subto.text_frame.paragraphs[0]
    p_st.text = "SUBMITTED TO:  DR. ARCHANA SASI"
    p_st.font.size = Pt(13)
    p_st.font.bold = True
    p_st.font.color.rgb = GREEN_ACCENT

    p_st2 = tb_subto.text_frame.add_paragraph()
    p_st2.text = "Course Coordinator / Faculty, Data Stream Analytics"
    p_st2.font.size = Pt(10)
    p_st2.font.color.rgb = TEXT_SUBTLE

    # Bottom note (NO academic year)
    tb_btm = slide1.shapes.add_textbox(Inches(1.2), Inches(6.95), Inches(11), Inches(0.4))
    p_b = tb_btm.text_frame.paragraphs[0]
    p_b.text = "Submitted in partial fulfillment of the requirements for the Data Stream Analytics Mini Project"
    p_b.font.size = Pt(10)
    p_b.font.italic = True
    p_b.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 2: PROBLEM STATEMENT & MOTIVATION
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide2, BG_LIGHT)
    add_header(slide2, "Problem Statement & Motivation", "CONTEXT & BACKGROUND")

    # Left: Traditional Batch Processing (Problem)
    add_card(slide2, Inches(0.8), Inches(1.5), Inches(5.7), Inches(5.3))
    strip1 = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.7), Inches(0.4))
    strip1.fill.solid()
    strip1.fill.fore_color.rgb = AMBER_ACCENT
    strip1.line.fill.background()

    tb2_left = slide2.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.3), Inches(4.6))
    tf2_l = tb2_left.text_frame
    tf2_l.word_wrap = True
    p = tf2_l.paragraphs[0]
    p.text = "Traditional Batch Processing (Delayed)"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = NAVY_DARK

    points_l = [
        "• IoT devices continuously generate high-velocity sensor data.",
        "• Traditional batch processing stores data first and analyzes it later.",
        "• Delayed analysis can miss abnormal equipment behavior during critical operations.",
        "• Static threshold rules (e.g. Temp > 50) fail to detect combinations of unusual sensor values.",
        "• Manual monitoring across multiple machines is slow, expensive, and impractical.",
    ]
    for pt in points_l:
        p = tf2_l.add_paragraph()
        p.text = pt
        p.font.size = Pt(12)
        p.font.color.rgb = TEXT_MAIN
        p.space_before = Pt(10)

    # Right: Real-Time Stream Processing (Need)
    add_card(slide2, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.3))
    strip2 = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.5), Inches(5.7), Inches(0.4))
    strip2.fill.solid()
    strip2.fill.fore_color.rgb = TEAL_ACCENT
    strip2.line.fill.background()

    tb2_right = slide2.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.6))
    tf2_r = tb2_right.text_frame
    tf2_r.word_wrap = True
    p = tf2_r.paragraphs[0]
    p.text = "Real-Time Streaming Approach (Our Goal)"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = NAVY_DARK

    points_r = [
        "• We need a system that analyzes sensor data as it arrives.",
        "• Real-time processing identifies abnormal behavior before hardware failures happen.",
        "• Machine learning evaluates multivariate combinations across sensor metrics.",
        "• Efficient DSA data structures keep streaming memory strictly bounded.",
        "• A live operator dashboard provides instant updates as new events are processed.",
    ]
    for pt in points_r:
        p = tf2_r.add_paragraph()
        p.text = pt
        p.font.size = Pt(12)
        p.font.color.rgb = TEXT_MAIN
        p.space_before = Pt(10)

    # =========================================================================
    # SLIDE 3: OBJECTIVES
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide3, BG_LIGHT)
    add_header(slide3, "Project Objectives", "PROJECT GOALS")

    objs = [
        ("1. Real-Time Streaming Pipeline", "Build a complete real-time streaming pipeline from data source to visualization."),
        ("2. Sensor Event Transport", "Use Apache Kafka to transport sensor events reliably as they are generated."),
        ("3. Efficient DSA Processing", "Apply DSA techniques (sliding windows, hash maps, heaps) for efficient stream processing."),
        ("4. Machine Learning Detection", "Detect abnormal sensor readings using an unsupervised Isolation Forest model."),
        ("5. Relational Data Storage", "Store processed readings, rolling metrics, and detected anomalies in MySQL."),
        ("6. Live Dashboard Visualization", "Display live streaming trends, metrics, and anomaly indicators using Streamlit."),
    ]
    for idx, (title, desc) in enumerate(objs):
        cx = Inches(0.8 + (idx % 2) * 6.0)
        cy = Inches(1.5 + (idx // 2) * 1.8)
        add_card(slide3, cx, cy, Inches(5.7), Inches(1.6))

        tb = slide3.shapes.add_textbox(cx + Inches(0.3), cy + Inches(0.15), Inches(5.1), Inches(1.3))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.size = Pt(13.5)
        p1.font.bold = True
        p1.font.color.rgb = BLUE_ACCENT

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(11)
        p2.font.color.rgb = TEXT_MAIN
        p2.space_before = Pt(4)

    # =========================================================================
    # SLIDE 4: SIX-LAYER ARCHITECTURE
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide4, BG_LIGHT)
    add_header(slide4, "Six-Layer System Architecture", "SYSTEM DESIGN")

    arch_img = os.path.abspath("docs/architecture.png")
    if os.path.exists(arch_img):
        slide4.shapes.add_picture(arch_img, Inches(0.8), Inches(1.4), Inches(7.2), Inches(5.5))

    # Right side: 6 Layers list
    add_card(slide4, Inches(8.3), Inches(1.4), Inches(4.2), Inches(5.5))
    tb_l = slide4.shapes.add_textbox(Inches(8.5), Inches(1.55), Inches(3.8), Inches(5.2))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True

    p = tf_l.paragraphs[0]
    p.text = "The Six Canonical Layers:"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = NAVY_DARK

    six_layers = [
        ("1. Data Source", "Simulated IoT sensor readings across 5 devices."),
        ("2. Streaming Tool", "Apache Kafka message broker for event transport."),
        ("3. Stream Processor", "Python consumer applying core DSA data structures."),
        ("4. ML Algorithm", "Isolation Forest for multivariate anomaly detection."),
        ("5. Database", "MySQL storing readings, rollups & anomalies."),
        ("6. Visualization", "Streamlit dashboard with live auto-refresh."),
    ]
    for l_num, l_desc in six_layers:
        p1 = tf_l.add_paragraph()
        p1.text = l_num
        p1.font.size = Pt(11)
        p1.font.bold = True
        p1.font.color.rgb = BLUE_ACCENT
        p1.space_before = Pt(7)

        p2 = tf_l.add_paragraph()
        p2.text = l_desc
        p2.font.size = Pt(10)
        p2.font.color.rgb = TEXT_MAIN

    # =========================================================================
    # SLIDE 5: DATA SOURCE AND STREAMING
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide5, BG_LIGHT)
    add_header(slide5, "Data Source and Streaming", "DATA INGESTION & TRANSPORT")

    # Left: Data Source
    add_card(slide5, Inches(0.8), Inches(1.5), Inches(5.7), Inches(5.3))
    strip5_1 = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.7), Inches(0.35))
    strip5_1.fill.solid()
    strip5_1.fill.fore_color.rgb = TEAL_ACCENT
    strip5_1.line.fill.background()

    tb5_l = slide5.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.3), Inches(4.6))
    tf5_l = tb5_l.text_frame
    tf5_l.word_wrap = True
    p = tf5_l.paragraphs[0]
    p.text = "IoT Sensor Data Simulation"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = NAVY_DARK

    pts5_l = [
        "• We simulate continuous IoT sensor readings.",
        "• 5 industrial devices are monitored (sensor-01 to sensor-05).",
        "• Sensors measure four physical parameters:",
        "    - Temperature (nominal 20 - 35 °C)",
        "    - Humidity (nominal 40 - 80 %)",
        "    - Pressure (nominal 1000 - 1025 hPa)",
        "    - Vibration (nominal 0.1 - 1.5 mm/s)",
        "• Dataset contains 5,000 records with millisecond timestamps.",
        "• Some unusual readings (~5%) are intentionally introduced for testing.",
    ]
    for pt in pts5_l:
        p = tf5_l.add_paragraph()
        p.text = pt
        p.font.size = Pt(11.5)
        p.font.color.rgb = TEXT_MAIN
        p.space_before = Pt(7)

    # Right: Kafka Streaming
    add_card(slide5, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.3))
    strip5_2 = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.5), Inches(5.7), Inches(0.35))
    strip5_2.fill.solid()
    strip5_2.fill.fore_color.rgb = BLUE_ACCENT
    strip5_2.line.fill.background()

    tb5_r = slide5.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.6))
    tf5_r = tb5_r.text_frame
    tf5_r.word_wrap = True
    p = tf5_r.paragraphs[0]
    p.text = "Apache Kafka Streaming"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = NAVY_DARK

    pts5_r = [
        "• Kafka sends sensor events one by one to the processing system.",
        "• Simple Event Flow:",
        "    Sensor Data → Kafka Producer → Kafka Topic",
        "• Producer dispatches records with pacing delay (0.5s) for live visibility.",
        "• Messages within a Kafka partition maintain their order of arrival,",
        "  helping preserve the sequence required for time-based stream processing.",
        "• Topic iot-sensor-events holds the active streaming queue.",
        "• Provides reliable, decoupled message transport without data loss.",
    ]
    for pt in pts5_r:
        p = tf5_r.add_paragraph()
        p.text = pt
        p.font.size = Pt(11.5)
        p.font.color.rgb = TEXT_MAIN
        p.space_before = Pt(7)

    # =========================================================================
    # SLIDE 6: STREAM PROCESSING USING DSA
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide6, BG_LIGHT)
    add_header(slide6, "Stream Processing Using DSA", "CORE DATA STRUCTURES")

    dsa_cards = [
        ("Deque / Sliding Window", "• Keeps the latest 30 sensor readings in a fixed-size window.\n• Used for calculating real-time rolling averages.\n• Efficiently removes old readings in O(1) time without list shifting.", TEAL_ACCENT),
        ("Hash Map / Dictionary", "• Keeps separate streaming information for each sensor device.\n• Allows fast O(1) average lookup and state update.\n• Organizes interleaved device streams cleanly.", BLUE_ACCENT),
        ("Priority Queue / Min-Heap", "• Keeps track of the most severe anomalies in O(log k) time.\n• Avoids sorting the entire history of thousands of events.\n• Keeps memory strictly bounded at O(k) capacity.", AMBER_ACCENT),
        ("Running Statistics", "• Maintains count, average, minimum, and maximum in O(1) time.\n• Updates summary values continuously as each event arrives.\n• Eliminates repeatedly re-scanning past records.", GREEN_ACCENT),
    ]
    for idx, (title, desc, color) in enumerate(dsa_cards):
        cx = Inches(0.8 + (idx % 2) * 6.0)
        cy = Inches(1.5 + (idx // 2) * 2.7)
        add_card(slide6, cx, cy, Inches(5.7), Inches(2.4))

        strip = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx, cy, Inches(5.7), Inches(0.35))
        strip.fill.solid()
        strip.fill.fore_color.rgb = color
        strip.line.fill.background()

        tb = slide6.shapes.add_textbox(cx + Inches(0.3), cy + Inches(0.45), Inches(5.1), Inches(1.8))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.size = Pt(14)
        p1.font.bold = True
        p1.font.color.rgb = NAVY_DARK

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(11)
        p2.font.color.rgb = TEXT_MAIN
        p2.space_before = Pt(8)

    # =========================================================================
    # SLIDE 7: ANOMALY DETECTION USING ISOLATION FOREST
    # =========================================================================
    slide7 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide7, BG_LIGHT)
    add_header(slide7, "Anomaly Detection Using Isolation Forest", "MACHINE LEARNING")

    # Left: Explanation
    add_card(slide7, Inches(0.8), Inches(1.5), Inches(6.0), Inches(5.3))
    tb7_l = slide7.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.6), Inches(4.9))
    tf7_l = tb7_l.text_frame
    tf7_l.word_wrap = True

    p = tf7_l.paragraphs[0]
    p.text = "Isolation Forest Machine Learning"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = NAVY_DARK

    pts7 = [
        "• Unsupervised Algorithm: Learns patterns from sensor data without requiring manual failure labels.",
        "• Multivariate Detection: Identifies unusual combinations of multiple sensor features (temperature, humidity, pressure, vibration).",
        "• Core Idea: Anomalous points are 'few and different' - they get isolated much faster in randomized decision trees.",
        "• Offline Training: The model is trained before live streaming starts and saved to disk.",
        "• Live Scoring: The trained model is then used to score incoming Kafka events immediately.",
        "• Contamination (0.05): Represents the expected proportion of anomalies used by the model to establish its decision boundary.",
    ]
    for pt in pts7:
        p = tf7_l.add_paragraph()
        p.text = pt
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_MAIN
        p.space_before = Pt(7)

    # Right: Visual Flow
    add_card(slide7, Inches(7.1), Inches(1.5), Inches(5.4), Inches(5.3))
    tb7_r = slide7.shapes.add_textbox(Inches(7.3), Inches(1.7), Inches(5.0), Inches(4.9))
    tf7_r = tb7_r.text_frame
    tf7_r.word_wrap = True

    p = tf7_r.paragraphs[0]
    p.text = "Simple Machine Learning Flow"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = BLUE_ACCENT

    flow_steps = [
        "Historical Sensor Data",
        "        ↓",
        "Train Model",
        "        ↓",
        "Saved Isolation Forest",
        "        ↓",
        "Incoming Kafka Event",
        "        ↓",
        "Anomaly Score",
        "        ↓",
        "Normal / Anomaly"
    ]
    for st in flow_steps:
        p = tf7_r.add_paragraph()
        p.text = st
        p.font.size = Pt(11)
        if "↓" in st:
            p.font.bold = True
            p.font.color.rgb = CYAN_ACCENT
            p.alignment = PP_ALIGN.CENTER
        else:
            p.font.bold = True
            p.font.color.rgb = NAVY_DARK
            p.alignment = PP_ALIGN.CENTER
        p.space_before = Pt(3)

    # =========================================================================
    # SLIDE 8: MYSQL DATABASE
    # =========================================================================
    slide8 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide8, BG_LIGHT)
    add_header(slide8, "MySQL Database Persistence", "DATA STORAGE")

    # Left: What is stored
    add_card(slide8, Inches(0.8), Inches(1.5), Inches(5.7), Inches(5.3))
    tb8_l = slide8.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.3), Inches(4.9))
    tf8_l = tb8_l.text_frame
    tf8_l.word_wrap = True

    p = tf8_l.paragraphs[0]
    p.text = "What MySQL Stores"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = BLUE_ACCENT

    pts8_l = [
        "MySQL stores the processed streaming information:",
        "• Sensor Readings:",
        "    Stores every processed event with device ID, sensor values, and timestamp.",
        "• Rolling Metrics:",
        "    Stores computed 30-reading rolling averages, minimums, and maximums.",
        "• Detected Anomalies:",
        "    Stores detected abnormal events with anomaly scores and severity level.",
    ]
    for pt in pts8_l:
        p = tf8_l.add_paragraph()
        p.text = pt
        p.font.size = Pt(11.5)
        p.font.color.rgb = TEXT_MAIN
        p.space_before = Pt(8)

    # Right: Why Database
    add_card(slide8, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.3))
    tb8_r = slide8.shapes.add_textbox(Inches(7.0), Inches(1.7), Inches(5.3), Inches(4.9))
    tf8_r = tb8_r.text_frame
    tf8_r.word_wrap = True

    p = tf8_r.paragraphs[0]
    p.text = "Why a Database is Used"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = TEAL_ACCENT

    pts8_r = [
        "• Keeps Historical Results:",
        "    Retains historical records for reporting, auditing, and trend analysis.",
        "• Separates Processing from Visualization:",
        "    Stream processing runs independently without UI query delays.",
        "• Fast Live Queries:",
        "    Allows the dashboard to quickly retrieve only recent readings.",
        "• Simple Architecture Flow:",
        "    Stream Processor  →  MySQL  →  Dashboard",
    ]
    for pt in pts8_r:
        p = tf8_r.add_paragraph()
        p.text = pt
        p.font.size = Pt(11.5)
        p.font.color.rgb = TEXT_MAIN
        p.space_before = Pt(8)

    # =========================================================================
    # SLIDE 9: REAL-TIME STREAMLIT DASHBOARD
    # =========================================================================
    slide9 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide9, BG_LIGHT)
    add_header(slide9, "Real-Time Streamlit Dashboard", "OPERATOR VISUALIZATION")

    features = [
        ("Current Sensor Values", "Displays real-time KPI cards for temperature, humidity, pressure, and vibration."),
        ("Total Readings & Anomalies", "Shows live counters for total processed events and detected abnormal readings."),
        ("Sensor Trends Over Time", "Interactive time-series charts display continuous physical sensor trends."),
        ("Rolling Average Overlays", "Plots actual readings against rolling averages to highlight gradual drifts."),
        ("Color-Coded Anomaly Flags", "Normal readings are marked in green; anomalies appear with prominent red badges."),
        ("Top Severe Anomalies Table", "Displays the most critical abnormal readings tracked by the priority queue."),
        ("Device Filter Control", "Allows the operator to focus on all devices or select an individual machine."),
        ("Automatic Refresh Loop", "Dashboard auto-refreshes periodically to reflect newly arrived stream records immediately."),
    ]
    for idx, (title, desc) in enumerate(features):
        cx = Inches(0.8 + (idx % 2) * 6.0)
        cy = Inches(1.5 + (idx // 2) * 1.35)
        add_card(slide9, cx, cy, Inches(5.7), Inches(1.2))

        tb = slide9.shapes.add_textbox(cx + Inches(0.2), cy + Inches(0.1), Inches(5.3), Inches(1.0))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.size = Pt(12)
        p1.font.bold = True
        p1.font.color.rgb = BLUE_ACCENT

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(10)
        p2.font.color.rgb = TEXT_MAIN
        p2.space_before = Pt(2)

    # =========================================================================
    # SLIDE 10: HOW THE SYSTEM WORKS (END-TO-END WORKFLOW)
    # =========================================================================
    slide10 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide10, BG_LIGHT)
    add_header(slide10, "How the System Works (End-to-End)", "LIVE PIPELINE WORKFLOW")

    add_card(slide10, Inches(0.8), Inches(1.5), Inches(11.7), Inches(5.3))
    tb10 = slide10.shapes.add_textbox(Inches(1.1), Inches(1.7), Inches(11.1), Inches(4.9))
    tf10 = tb10.text_frame
    tf10.word_wrap = True

    p = tf10.paragraphs[0]
    p.text = "Complete Data Movement Flow:"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = BLUE_ACCENT

    p_flow = tf10.add_paragraph()
    p_flow.text = "IoT Data  →  Kafka Producer  →  Kafka Topic  →  Stream Processor  →  DSA + Isolation Forest  →  MySQL  →  Streamlit Dashboard"
    p_flow.font.size = Pt(11)
    p_flow.font.bold = True
    p_flow.font.color.rgb = NAVY_DARK
    p_flow.space_before = Pt(4)

    steps_all = [
        ("Data is Generated", "IoT sensor data is generated with simulated physical readings and test anomalies."),
        ("Events Sent Through Kafka", "The Kafka Producer sends sensor events one by one to the message topic."),
        ("Immediate Event Processing", "Each event is processed immediately as it arrives without waiting for batches."),
        ("DSA State Maintenance", "Sliding window deque updates rolling values; hash map organizes per-device state."),
        ("ML Anomaly Detection", "Isolation Forest detects multivariate anomalies across multiple sensor variables."),
        ("Priority Queue Ranking", "A min-heap keeps track of the most severe anomalies without sorting all history."),
        ("Database Persistence", "Processed readings, rolling averages, and anomaly flags are stored in MySQL."),
        ("Live Visual Display", "Dashboard automatically displays updated results as new data arrives."),
    ]
    for s_title, s_desc in steps_all:
        p = tf10.add_paragraph()
        p.text = f"• {s_title}: {s_desc}"
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_MAIN
        p.space_before = Pt(5)

    # =========================================================================
    # SLIDE 11: RESULTS, TESTING & ADVANTAGES
    # =========================================================================
    slide11 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide11, BG_LIGHT)
    add_header(slide11, "Results, Testing and Advantages", "VERIFIED RESULTS")

    # Left: Test Results
    add_card(slide11, Inches(0.8), Inches(1.5), Inches(5.7), Inches(5.3))
    tb11_l = slide11.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.3), Inches(4.9))
    tf11_l = tb11_l.text_frame
    tf11_l.word_wrap = True

    p = tf11_l.paragraphs[0]
    p.text = "Verified Automated Testing"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = GREEN_ACCENT

    tests_list = [
        "• Automated Test Suite: 31 / 31 tests passed (100%)",
        "• What Was Tested and Verified:",
        "    - Sliding-window functionality (FIFO eviction & rolling avg)",
        "    - Running statistics accumulators (mean, min, max)",
        "    - Heap/top-K anomaly tracking tested",
        "    - Dataset generation tested (ranges & test anomalies)",
        "    - DSA integration tested across live stream processing path",
        "• Zero test failures across all automated test suites.",
    ]
    for t in tests_list:
        p = tf11_l.add_paragraph()
        p.text = t
        p.font.size = Pt(11.5)
        p.font.color.rgb = TEXT_MAIN
        p.space_before = Pt(8)

    # Right: Advantages
    add_card(slide11, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.3))
    tb11_r = slide11.shapes.add_textbox(Inches(7.0), Inches(1.7), Inches(5.3), Inches(4.9))
    tf11_r = tb11_r.text_frame
    tf11_r.word_wrap = True

    p = tf11_r.paragraphs[0]
    p.text = "System Advantages"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = BLUE_ACCENT

    advs_list = [
        "• Real-Time Processing: Analyzes sensor events immediately as they arrive.",
        "• Bounded Memory Usage: Sliding windows and heaps keep memory strictly bounded.",
        "• Automated Anomaly Detection: Machine learning identifies abnormal multi-sensor patterns.",
        "• Live Visualization: Streamlit interface gives operators immediate visibility.",
        "• Modular Six-Layer Architecture: Components are decoupled, clean, and maintainable.",
    ]
    for a in advs_list:
        p = tf11_r.add_paragraph()
        p.text = a
        p.font.size = Pt(11.5)
        p.font.color.rgb = TEXT_MAIN
        p.space_before = Pt(8)

    # =========================================================================
    # SLIDE 12: CONCLUSION & THANK YOU
    # =========================================================================
    slide12 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide12, NAVY_DARK)

    accent_bar12 = slide12.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(0.4), SLIDE_HEIGHT)
    accent_bar12.fill.solid()
    accent_bar12.fill.fore_color.rgb = BLUE_ACCENT
    accent_bar12.line.fill.background()

    # Left: Conclusion points
    add_card(slide12, Inches(1.0), Inches(1.2), Inches(6.8), Inches(5.5), NAVY_CARD, RGBColor(51, 65, 85))
    tb12_l = slide12.shapes.add_textbox(Inches(1.3), Inches(1.5), Inches(6.2), Inches(5.0))
    tf12_l = tb12_l.text_frame
    tf12_l.word_wrap = True

    p = tf12_l.paragraphs[0]
    p.text = "Project Conclusion"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT

    conc_points = [
        "• Successfully implemented a six-layer real-time streaming analytics system.",
        "• Kafka enables reliable, decoupled event streaming.",
        "• DSA structures (deque, hash map, heap) make stream processing efficient.",
        "• Isolation Forest detects unusual sensor behavior across multiple variables.",
        "• MySQL stores processed results and rolling window metrics.",
        "• Streamlit provides live, auto-refreshing visualization for monitoring.",
    ]
    for c in conc_points:
        p = tf12_l.add_paragraph()
        p.text = c
        p.font.size = Pt(12)
        p.font.color.rgb = TEXT_SUBTLE
        p.space_before = Pt(10)

    # Right: Thank you & Questions
    add_card(slide12, Inches(8.2), Inches(1.2), Inches(4.3), Inches(5.5), NAVY_CARD, RGBColor(51, 65, 85))
    tb12_r = slide12.shapes.add_textbox(Inches(8.4), Inches(2.3), Inches(3.9), Inches(3.5))
    tf12_r = tb12_r.text_frame
    tf12_r.word_wrap = True

    p = tf12_r.paragraphs[0]
    p.text = "THANK YOU!"
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p.alignment = PP_ALIGN.CENTER

    p2 = tf12_r.add_paragraph()
    p2.text = "QUESTIONS?"
    p2.font.size = Pt(18)
    p2.font.bold = True
    p2.font.color.rgb = CYAN_ACCENT
    p2.alignment = PP_ALIGN.CENTER
    p2.space_before = Pt(20)

    p3 = tf12_r.add_paragraph()
    p3.text = "Data Stream Analytics Mini Project\nGroup No: 3"
    p3.font.size = Pt(12)
    p3.font.color.rgb = TEXT_MUTED
    p3.alignment = PP_ALIGN.CENTER
    p3.space_before = Pt(30)

    # Save presentation
    output_pptx = os.path.abspath("docs/DSA_Mini_Project_Presentation.pptx")
    prs.save(output_pptx)
    print(f"Presentation saved to: {output_pptx}")
    print(f"Total Slides: {len(prs.slides)}")


if __name__ == "__main__":
    create_presentation()
