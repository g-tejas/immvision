import typing
import numpy as np
from .cv_types import *

# <autogen:pyi> // Autogenerated code below. Do not edit!

class ColormapScaleFromStatsData:
    " Scale the Colormap according to the Image  stats"
    
    # Are we using the stats on the full image?
    # If ActiveOnFullImage and ActiveOnROI are both false, then ColormapSettingsData.ColormapScaleMin/Max will be used
    active_on_full_image: bool = True
    # Are we using the stats on the ROI?
    # If ActiveOnFullImage and ActiveOnROI are both false, then ColormapSettingsData.ColormapScaleMin/Max will be used
    # Note: ActiveOnROI and ActiveOnFullImage cannot be true at the same time!
    active_on_roi: bool = False
    # If active (either on ROI or on Image), how many sigmas around the mean should the Colormap be applied
    nb_sigmas: float = 1.5
    # If UseStatsMin is true, then ColormapScaleMin will be calculated from the matrix min value instead of a sigma based value
    use_stats_min: bool = False
    # If UseStatsMin is true, then ColormapScaleMax will be calculated from the matrix max value instead of a sigma based value
    use_stats_max: bool = False


class ColormapSettingsData:
    " Colormap Settings (useful for matrices with one channel, in order to see colors mapping float values)"
    
    # Colormap, see available Colormaps with AvailableColormaps()
    # Work only with 1 channel matrices, i.e len(shape)==2
    colormap: str = "None"
    # ColormapScaleMin and ColormapScaleMax indicate how the Colormap is applied:
    # - Values in [ColormapScaleMin, ColomapScaleMax] will use the full colormap.
    # - Values outside this interval will be clamped before coloring
    # by default, the initial values are ignored, and they will be updated automatically
    # via the options in ColormapScaleFromStats
    colormap_scale_min: float = 0.
    # 
    colormap_scale_max: float = 1.
    # If ColormapScaleFromStats.ActiveOnFullImage or ColormapScaleFromStats.ActiveOnROI,
    # then ColormapScaleMin/Max are ignored, and the scaling is done according to the image stats.
    # ColormapScaleFromStats.ActiveOnFullImage is true by default
    colormap_scale_from_stats: ColormapScaleFromStatsData = ColormapScaleFromStatsData()
    # Internal value: stores the name of the Colormap that is hovered by the mouse
    internal_colormap_hovered: str = ""


class MouseInformation:
    " Contains information about the mouse inside an image"
    
    # Is the mouse hovering the image
    is_mouse_hovering: bool = False
    # Mouse position in the original image/matrix
    # This position is given with float coordinates, and will be (-1., -1.) if the mouse is not hovering the image
    mouse_position: Point2d = (-1., -1.)
    # Mouse position in the displayed portion of the image (the original image can be zoomed,
    # and only show a subset if it may be shown).
    # This position is given with integer coordinates, and will be (-1, -1) if the mouse is not hovering the image
    mouse_position_displayed: Point = (-1, -1)

    #
    #  Note: you can query ImGui::IsMouseDown(mouse_button) (c++) or imgui.is_mouse_down(mouse_button) (Python)
    #


class ImageParams:
    " Set of display parameters and options for an Image"
    

    #
    #  ImageParams store the parameters for a displayed image
    #  (as well as user selected watched pixels, selected channel, etc.)
    #  Its default constructor will give them reasonable choices, which you can adapt to your needs.
    #  Its values will be updated when the user pans or zooms the image, adds watched pixels, etc.
    #

    #
    #  Refresh Images Textures
    #
    # Refresh Image: images textures are cached. Set to true if your image matrix/buffer has changed
    # (for example, for live video images)
    refresh_image: bool = False

    #
    #  Display size and title
    #
    # Size of the displayed image (can be different from the matrix size)
    # If you specify only the width or height (e.g (300, 0), then the other dimension
    # will be calculated automatically, respecting the original image w/h ratio.
    image_display_size: Size = (0, 0)

    #
    #  Zoom and Pan (represented by an affine transform matrix, of size 3x3)
    #
    # ZoomPanMatrix can be created using MakeZoomPanMatrix to create a view centered around a given point
    zoom_pan_matrix: Matx33d = np.eye(3)
    # If displaying several images, those with the same ZoomKey will zoom and pan together
    zoom_key: str = ""

    #
    #  Colormap Settings (useful for matrices with one channel, in order to see colors mapping float values)
    #
    # ColormapSettings stores all the parameter concerning the Colormap
    colormap_settings: ColormapSettingsData = ColormapSettingsData()
    # If displaying several images, those with the same ColormapKey will adjust together
    colormap_key: str = ""

    #
    #  Zoom and pan with the mouse
    #
    # 
    pan_with_mouse: bool = True
    # 
    zoom_with_mouse_wheel: bool = True
    # Color Order: RGB or RGBA versus BGR or BGRA (Note: by default OpenCV uses BGR and BGRA)
    is_color_order_bgr: bool = True

    #
    #  Image display options
    #
    # if SelectedChannel >= 0 then only this channel is displayed
    selected_channel: int = -1
    # Show a "school paper" background grid
    show_school_paper_background: bool = True
    # show a checkerboard behind transparent portions of 4 channels RGBA images
    show_alpha_channel_checkerboard: bool = True
    # Grid displayed when the zoom is high
    show_grid: bool = True
    # Pixel values show when the zoom is high
    draw_values_on_zoomed_pixels: bool = True

    #
    #  Image display options
    #
    # Show matrix type and size
    show_image_info: bool = True
    # Show pixel values
    show_pixel_info: bool = True
    # Show buttons that enable to zoom in/out (the mouse wheel also zoom)
    show_zoom_buttons: bool = True
    # Open the options panel
    show_options_panel: bool = False
    # If set to true, then the option panel will be displayed in a transient tooltip window
    show_options_in_tooltip: bool = False
    # If set to false, then the Options button will not be displayed
    show_options_button: bool = True

    #
    #  Watched Pixels
    #
    # List of Watched Pixel coordinates
    watched_pixels: list[Point] = list[Point]()
    # Shall we add a watched pixel on double click
    add_watched_pixel_on_double_click: bool = True
    # Shall the watched pixels be drawn on the image
    highlight_watched_pixels: bool = True
    # Mouse position information. These values are filled after displaying an image
    mouse_info: MouseInformation = MouseInformation()



# </autogen:pyi> // Autogenerated code end
