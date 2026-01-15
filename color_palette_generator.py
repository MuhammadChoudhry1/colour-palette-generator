import tkinter as tk
from tkinter import ttk, messagebox
import colorsys
import re


class ColorPaletteGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("🎨 Color Palette Generator")
        self.root.geometry("1000x750")
        self.root.minsize(900, 650)
        self.root.resizable(True, True)
        self.root.configure(bg='#0f0f1e')
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure custom styles
        style.configure('Title.TLabel', background='#1a1a2e', foreground='#eee', 
                       font=('Segoe UI', 28, 'bold'))
        style.configure('Subtitle.TLabel', background='#1a1a2e', foreground='#aaa', 
                       font=('Segoe UI', 10))
        style.configure('Custom.TFrame', background='#1a1a2e')
        style.configure('Input.TFrame', background='#16213e', relief='flat')
        style.configure('Custom.TEntry', fieldbackground='#16213e', foreground='#eee',
                       borderwidth=0, relief='flat')
        style.configure('Custom.TButton', background='#0f4c75', foreground='white',
                       borderwidth=0, relief='flat', font=('Segoe UI', 11, 'bold'))
        style.map('Custom.TButton',
                 background=[('active', '#3282b8'), ('pressed', '#0f4c75')])
        
        # Main container with gradient effect
        main_frame = tk.Frame(root, bg='#0f0f1e', padx=35, pady=35)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Store main frame reference for responsive updates
        self.main_frame = main_frame
        
        # Animated gradient header with glassmorphism
        self.header_canvas = tk.Canvas(main_frame, height=160, bg='#0f0f1e', highlightthickness=0)
        self.header_canvas.pack(fill=tk.X, pady=(0, 35))
        
        # Initial header draw
        self.draw_header()
        
        self.header_canvas.bind('<Configure>', self.on_header_resize)
        
        # Input section with glassmorphism card
        input_container = tk.Frame(main_frame, bg='#0f0f1e')
        input_container.pack(fill=tk.X, pady=(0, 30))
        
        # Create rounded card effect
        self.input_canvas = tk.Canvas(input_container, height=140, bg='#0f0f1e', highlightthickness=0)
        self.input_canvas.pack(fill=tk.X)
        
        # Bind resize event for input canvas
        self.input_canvas.bind('<Configure>', self.on_input_resize)
        
        input_frame = tk.Frame(input_container, bg='#0f0f1e')
        input_frame.pack(fill=tk.X, padx=35, pady=25)
        self.input_frame = input_frame
        
        # Input label with icon
        label_frame = tk.Frame(input_frame, bg='#0f0f1e')
        label_frame.pack(anchor='w', pady=(0, 12))
        
        tk.Label(label_frame, text="🎯", font=('Segoe UI', 16), bg='#0f0f1e').pack(side=tk.LEFT)
        tk.Label(label_frame, text="Enter Your Color", font=('Segoe UI', 14, 'bold'), 
                bg='#0f0f1e', fg='#ffffff').pack(side=tk.LEFT, padx=(8, 0))
        
        # Entry and button container
        entry_button_frame = tk.Frame(input_frame, bg='#0f0f1e')
        entry_button_frame.pack(fill=tk.X)
        
        # Custom styled entry with glow effect
        entry_outer = tk.Frame(entry_button_frame, bg='#6a11cb', bd=0)
        entry_outer.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 15), ipady=1, ipadx=1)
        
        entry_wrapper = tk.Frame(entry_outer, bg='#1a1a35', bd=0)
        entry_wrapper.pack(fill=tk.BOTH, expand=True)
        
        self.color_input = tk.Entry(entry_wrapper, font=('Segoe UI', 14), width=30,
                                   bg='#1a1a35', fg='#ffffff', bd=0, insertbackground='#6a11cb',
                                   relief='flat')
        self.color_input.pack(padx=15, pady=12, fill=tk.X)
        self.color_input.insert(0, "#3498db")
        
        # Show color preview
        self.color_preview = tk.Frame(entry_button_frame, width=50, height=50, bg='#3498db', bd=0)
        self.color_preview.pack(side=tk.LEFT, padx=(0, 15))
        self.color_preview.pack_propagate(False)
        
        # Bind events
        self.color_input.bind('<Return>', lambda e: self.generate_palettes())
        self.color_input.bind('<KeyRelease>', self.update_preview)
        
        # Gradient button
        btn_canvas = tk.Canvas(entry_button_frame, width=180, height=50, bg='#0f0f1e', 
                              highlightthickness=0, cursor='hand2')
        btn_canvas.pack(side=tk.LEFT)
        
        self.create_gradient(btn_canvas, 0, 0, 180, 50, '#ff6b6b', '#ee5a6f')
        btn_canvas.create_text(90, 25, text="✨ Generate", font=('Segoe UI', 13, 'bold'), 
                              fill='white', tags='btn_text')
        
        btn_canvas.bind('<Button-1>', lambda e: self.generate_palettes())
        btn_canvas.bind('<Enter>', lambda e: btn_canvas.config(cursor='hand2'))
        
        # Info label
        info_text = "💡 Hex (#3498db), RGB (rgb(52,152,219)), or color name (blue) • Click colors to copy"
        tk.Label(input_frame, text=info_text, font=('Segoe UI', 9), 
                bg='#0f0f1e', fg='#7a7a8c').pack(pady=(12, 0))
        
        # Scrollable palette display frame
        canvas_frame = tk.Frame(main_frame, bg='#0f0f1e')
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        # Canvas with scrollbar
        self.canvas = tk.Canvas(canvas_frame, bg='#0f0f1e', highlightthickness=0)
        scrollbar = tk.Scrollbar(canvas_frame, orient='vertical', command=self.canvas.yview,
                                bg='#1a1a2e', troughcolor='#0f0f1e', width=12)
        self.palette_frame = tk.Frame(self.canvas, bg='#0f0f1e')
        
        self.palette_frame.bind('<Configure>', 
                               lambda e: self.canvas.configure(scrollregion=self.canvas.bbox('all')))
        
        self.canvas.create_window((0, 0), window=self.palette_frame, anchor='nw')
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Mouse wheel scrolling
        self.canvas.bind_all('<MouseWheel>', self._on_mousewheel)
        
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), 'units')
    
    def draw_header(self):
        """Draw header with proper centering"""
        canvas = self.header_canvas
        width = canvas.winfo_width() if canvas.winfo_width() > 1 else 1000
        
        canvas.delete('all')
        self.create_gradient(canvas, 0, 0, width, 160, '#6a11cb', '#2575fc')
        
        # Centered text
        center_x = width // 2
        canvas.create_text(center_x, 60, text="🎨 COLOR PALETTE", 
                          font=('Segoe UI', 38, 'bold'), fill='#ffffff')
        canvas.create_text(center_x, 105, 
                          text="✨ Create stunning color schemes in seconds ✨", 
                          font=('Segoe UI', 12), fill='#e0e0e0')
        
        # Decorative circles (positioned relative to width)
        canvas.create_oval(50, 30, 80, 60, fill='#ff6b6b', outline='')
        if width > 200:
            canvas.create_oval(width-80, 100, width-50, 130, fill='#4ecdc4', outline='')
            canvas.create_oval(width-150, 20, width-130, 40, fill='#ffe66d', outline='')
    
    def create_gradient(self, canvas, x1, y1, x2, y2, color1, color2):
        """Create a gradient on canvas"""
        r1, g1, b1 = self.hex_to_rgb(color1)
        r2, g2, b2 = self.hex_to_rgb(color2)
        
        height = y2 - y1
        for i in range(height):
            ratio = i / height
            r = int(r1 * 255 * (1 - ratio) + r2 * 255 * ratio)
            g = int(g1 * 255 * (1 - ratio) + g2 * 255 * ratio)
            b = int(b1 * 255 * (1 - ratio) + b2 * 255 * ratio)
            color = f'#{r:02x}{g:02x}{b:02x}'
            canvas.create_line(x1, y1 + i, x2, y1 + i, fill=color, width=1)
    
    def on_header_resize(self, event):
        """Handle header canvas resize"""
        self.root.after(10, self.draw_header)
    
    def on_input_resize(self, event):
        """Handle input canvas resize"""
        canvas = event.widget
        width = event.width
        canvas.delete('all')
        # Draw responsive rounded rectangle
        canvas.create_rectangle(5, 5, width-5, 135, fill='#1a1a2e', outline='#2575fc', width=2)
        
        # Generate initial palette
        self.generate_palettes()
    
    def hex_to_rgb(self, hex_color):
        """Convert hex color to RGB tuple (0-1 range)"""
        hex_color = hex_color.lstrip('#')
        if len(hex_color) == 3:
            hex_color = ''.join([c*2 for c in hex_color])
        return tuple(int(hex_color[i:i+2], 16)/255.0 for i in (0, 2, 4))
    
    def rgb_to_hex(self, rgb):
        """Convert RGB tuple (0-1 range) to hex color"""
        return '#%02x%02x%02x' % tuple(int(c*255) for c in rgb)
    
    def adjust_hue(self, h, s, v, hue_shift):
        """Adjust hue by a certain amount"""
        new_h = (h + hue_shift) % 1.0
        return colorsys.hsv_to_rgb(new_h, s, v)
    
    def update_preview(self, event=None):
        """Update color preview as user types"""
        try:
            color = self.parse_color_input(self.color_input.get())
            if color:
                self.color_preview.config(bg=color)
        except:
            pass
    
    def parse_color_input(self, color_str):
        """Parse color input (hex or name) and return hex color"""
        color_str = color_str.strip().lower()
        
        # Common color names
        color_names = {
            'red': '#FF0000', 'green': '#00FF00', 'blue': '#0000FF',
            'yellow': '#FFFF00', 'cyan': '#00FFFF', 'magenta': '#FF00FF',
            'black': '#000000', 'white': '#FFFFFF', 'gray': '#808080',
            'orange': '#FFA500', 'purple': '#800080', 'pink': '#FFC0CB',
            'brown': '#A52A2A', 'lime': '#00FF00', 'navy': '#000080',
            'teal': '#008080', 'olive': '#808000', 'maroon': '#800000',
            'aqua': '#00FFFF', 'silver': '#C0C0C0', 'gold': '#FFD700'
        }
        
        if color_str in color_names:
            return color_names[color_str]
        
        # Check if it's a valid hex color
        if re.match(r'^#?([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$', color_str):
            return '#' + color_str.lstrip('#')
        
        return None
    
    def generate_palettes(self):
        """Generate various color palettes"""
        # Clear previous palettes
        for widget in self.palette_frame.winfo_children():
            widget.destroy()
        
        # Parse input color
        base_color = self.parse_color_input(self.color_input.get())
        
        if not base_color:
            messagebox.showerror("Invalid Color", 
                               "Please enter a valid hex color (#RRGGBB) or color name")
            return
        
        # Convert to RGB and HSV
        rgb = self.hex_to_rgb(base_color)
        h, s, v = colorsys.rgb_to_hsv(*rgb)
        
        # Define palette types
        palettes = {
            "Base Color": [base_color],
            "Complementary": [
                base_color,
                self.rgb_to_hex(self.adjust_hue(h, s, v, 0.5))
            ],
            "Analogous": [
                self.rgb_to_hex(self.adjust_hue(h, s, v, -0.083)),
                base_color,
                self.rgb_to_hex(self.adjust_hue(h, s, v, 0.083))
            ],
            "Triadic": [
                base_color,
                self.rgb_to_hex(self.adjust_hue(h, s, v, 0.333)),
                self.rgb_to_hex(self.adjust_hue(h, s, v, 0.667))
            ],
            "Split Complementary": [
                base_color,
                self.rgb_to_hex(self.adjust_hue(h, s, v, 0.417)),
                self.rgb_to_hex(self.adjust_hue(h, s, v, 0.583))
            ],
            "Monochromatic": [
                self.rgb_to_hex(colorsys.hsv_to_rgb(h, s, v * 0.4)),
                self.rgb_to_hex(colorsys.hsv_to_rgb(h, s, v * 0.7)),
                base_color,
                self.rgb_to_hex(colorsys.hsv_to_rgb(h, s * 0.7, min(v * 1.3, 1.0))),
                self.rgb_to_hex(colorsys.hsv_to_rgb(h, s * 0.4, min(v * 1.6, 1.0)))
            ]
        }
        
        # Display each palette
        for idx, (palette_name, colors) in enumerate(palettes.items()):
            self.create_palette_display(self.palette_frame, palette_name, colors, idx)
    
    def create_palette_display(self, parent, name, colors, row):
        """Create a palette display with color swatches"""
        # Outer card with glow effect
        card_outer = tk.Frame(parent, bg='#0f0f1e', pady=2)
        card_outer.pack(fill=tk.X, pady=10)
        
        # Inner card with glassmorphism
        card = tk.Frame(card_outer, bg='#1a1a35', pady=25, padx=25, relief=tk.FLAT)
        card.pack(fill=tk.BOTH, expand=True)
        
        # Header frame
        header = tk.Frame(card, bg='#1a1a35')
        header.pack(fill=tk.X, pady=(0, 18))
        
        # Palette name with icon and gradient accent
        icons = {'Base Color': '⭐', 'Complementary': '🔄', 'Analogous': '〰️',
                'Triadic': '🔺', 'Split Complementary': '↔️', 'Monochromatic': '🌈'}
        icon = icons.get(name, '●')
        
        icon_colors = {'Base Color': '#ff6b6b', 'Complementary': '#4ecdc4', 
                      'Analogous': '#ffe66d', 'Triadic': '#a8e6cf', 
                      'Split Complementary': '#ffa07a', 'Monochromatic': '#dda0dd'}
        accent_color = icon_colors.get(name, '#6a11cb')
        
        # Colored accent bar
        accent = tk.Frame(header, bg=accent_color, width=5, height=30)
        accent.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 12))
        
        name_label = tk.Label(header, text=f"{icon} {name}", 
                             font=('Segoe UI', 16, 'bold'), 
                             bg='#1a1a35', fg='#ffffff', anchor='w')
        name_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Color count badge
        count_badge = tk.Label(header, text=f"{len(colors)} colors", 
                              font=('Segoe UI', 9), bg='#2a2a45', fg='#aaa',
                              padx=10, pady=3)
        count_badge.pack(side=tk.RIGHT)
        
        # Color swatches container - responsive grid
        swatch_frame = tk.Frame(card, bg='#1a1a35')
        swatch_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configure grid for responsive layout
        for i in range(len(colors)):
            swatch_frame.grid_columnconfigure(i, weight=1, uniform='color')
        
        for idx, color in enumerate(colors):
            # Swatch container
            swatch_container = tk.Frame(swatch_frame, bg='#1a1a35')
            swatch_container.grid(row=0, column=idx, padx=5, sticky='nsew')
            
            # Create canvas for rounded corners and shadow
            swatch_canvas = tk.Canvas(swatch_container, height=110, 
                                     bg='#1a1a35', highlightthickness=0)
            swatch_canvas.pack(fill=tk.BOTH, expand=True)
            
            # Bind configure to redraw on resize
            swatch_canvas.bind('<Configure>', 
                             lambda e, c=color, canvas=swatch_canvas: self.draw_swatch(canvas, c))
            
            # Store color
            swatch_canvas.color = color
            
            # Click to copy
            swatch_canvas.bind('<Button-1>', 
                             lambda e, canvas=swatch_canvas: self.copy_to_clipboard(canvas.color, canvas))
    
    def get_contrast_color(self, hex_color):
        """Get contrasting text color (black or white) for readability"""
        rgb = self.hex_to_rgb(hex_color)
        luminance = 0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]
        return '#000000' if luminance > 0.5 else '#FFFFFF'
    
    def darken_color(self, hex_color, factor=0.6):
        """Darken a color by a factor"""
        rgb = self.hex_to_rgb(hex_color)
        darkened = tuple(c * factor for c in rgb)
        return self.rgb_to_hex(darkened)
    
    def draw_swatch(self, canvas, color):
        """Draw a color swatch that adapts to canvas size"""
        width = canvas.winfo_width() if canvas.winfo_width() > 1 else 120
        height = 110
        
        canvas.delete('all')
        
        # Shadow effect
        canvas.create_rectangle(3, 103, width-3, 109, fill='#0a0a14', outline='')
        
        # Main color rectangle
        canvas.create_rectangle(0, 0, width, 100, fill=color, outline='', tags='swatch')
        
        # Color info overlay at bottom
        overlay_color = self.darken_color(color)
        canvas.create_rectangle(0, 70, width, 100, fill=overlay_color, outline='', tags='overlay')
        
        # Color hex text (centered)
        center_x = width // 2
        canvas.create_text(center_x, 85, text=color.upper(), 
                          font=('Consolas', 11, 'bold'),
                          fill='#ffffff', tags='hex_text')
        
        # Add copy icon (initially hidden)
        canvas.create_text(center_x, 35, text="📋", font=('Segoe UI', 20), 
                          fill=overlay_color, tags='copy_icon')
        
        # Hover and click effects
        def on_enter(e):
            overlay = self.darken_color(color, 0.3)
            canvas.itemconfig('overlay', fill=overlay)
            canvas.itemconfig('copy_icon', fill='#ffffff')
            canvas.config(cursor='hand2')
        
        def on_leave(e):
            overlay = self.darken_color(color)
            canvas.itemconfig('overlay', fill=overlay)
            canvas.itemconfig('copy_icon', fill=overlay)
        
        canvas.bind('<Enter>', on_enter)
        canvas.bind('<Leave>', on_leave)
    
    def copy_to_clipboard(self, color, swatch=None):
        """Copy color to clipboard with visual feedback"""
        self.root.clipboard_clear()
        self.root.clipboard_append(color)
        self.root.update()
        
        # Visual feedback
        if swatch:
            original_relief = swatch.cget('relief')
            swatch.config(relief=tk.SUNKEN, borderwidth=3)
            self.root.after(200, lambda: swatch.config(relief=tk.FLAT, borderwidth=0))
        
        # Create custom notification
        self.show_notification(f"✓ {color.upper()} copied!")
    
    def show_notification(self, message):
        """Show a temporary notification with animation"""
        notif = tk.Toplevel(self.root)
        notif.overrideredirect(True)
        notif.attributes('-topmost', True)
        notif.attributes('-alpha', 0.0)
        
        # Position at bottom center
        notif_width = 300
        notif_height = 60
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (notif_width // 2)
        y = self.root.winfo_y() + self.root.winfo_height() - 120
        notif.geometry(f"{notif_width}x{notif_height}+{x}+{y}")
        
        # Create canvas with gradient
        canvas = tk.Canvas(notif, width=notif_width, height=notif_height, 
                          bg='#0f0f1e', highlightthickness=0)
        canvas.pack()
        
        # Gradient background
        self.create_gradient(canvas, 0, 0, notif_width, notif_height, '#4ecdc4', '#44a8a0')
        
        # Message text (single, clean)
        canvas.create_text(notif_width//2, notif_height//2, text=message,
                          font=('Segoe UI', 12, 'bold'), fill='white')
        
        # Fade in animation
        def fade_in(alpha=0.0):
            if alpha < 0.95:
                notif.attributes('-alpha', alpha)
                self.root.after(20, lambda: fade_in(alpha + 0.1))
        
        # Fade out animation
        def fade_out(alpha=0.95):
            if alpha > 0:
                notif.attributes('-alpha', alpha)
                self.root.after(20, lambda: fade_out(alpha - 0.1))
            else:
                notif.destroy()
        
        fade_in()
        self.root.after(1500, fade_out)


def main():
    root = tk.Tk()
    app = ColorPaletteGenerator(root)
    root.mainloop()


if __name__ == "__main__":
    main()
