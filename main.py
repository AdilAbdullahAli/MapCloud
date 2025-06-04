import cv2
import os
pip install opencv-python

import cv2
import os
video_file = r"C:\Users\adila\Videos\Captures\geo.mp4"
output_folder = r"C:\Users\adila\Videos\Captures\ExtractedFrames"
def extract_frames(video_path, output_folder, frames_per_second=1):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video {video_path}")
        return

import cv2
import os
video_file = r"C:\Users\adila\Videos\Captures\geo.mp4"
output_folder = r"C:\Users\adila\Videos\Captures\ExtractedFrames"

def extract_frames(video_path, output_folder, frames_per_second=1):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created output folder: {output_folder}")
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"Error: Could not open video: {video_path}")
        return


    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0:
        print("Error: Could not retrieve video FPS.")
        cap.release() 
        return

    frame_interval = int(fps / frames_per_second)
    if frame_interval == 0:
        frame_interval = 1

    frame_count = 0
    success, image = cap.read()

    print(f"Extracting frames from {video_path} at {frames_per_second} FPS...")

    while success:
        if frame_count % frame_interval == 0:
            frame_filename = os.path.join(output_folder, f"frame_{frame_count:05d}.png")
            cv2.imwrite(frame_filename, image)
        success, image = cap.read()
        frame_count += 1

    cap.release()
    print(f"Finished extracting frames to {output_folder}. Total frames processed: {frame_count // frame_interval} (at {frames_per_second} FPS)")


# Call the function with your specified paths
extract_frames(video_file, output_folder, frames_per_second=5)
pip install folium

import cv2
import os
import glob
def stitch_images_with_opencv(image_folder, output_stitched_image="stitched_panorama.png"):
    images = []
    image_paths = sorted(glob.glob(os.path.join(image_folder, "*.png")))

    if not image_paths:
        print(f"Error: No PNG images found in {image_folder}")
        return

    print(f"Loading {len(image_paths)} images from {image_folder}...")
    for path in image_paths:
        img = cv2.imread(path)
        if img is None:
            print(f"Warning: Could not load image {path}. Skipping.")
            continue
        images.append(img)

    if not images:
        print("No valid images to stitch.")
        return
    stitcher = cv2.Stitcher.create(cv2.Stitcher_PANORAMA) # Or cv2.Stitcher_SCANS
    print("Attempting to stitch images...")
    status, stitched_image = stitcher.stitch(images)
    if status == cv2.Stitcher_OK:
        print("Stitching successful!")
        cv2.imwrite(output_stitched_image, stitched_image)
        print(f"Stitched image saved to {output_stitched_image}")
    else:
        print(f"Stitching failed! Error code: {status}")
        if status == cv2.Stitcher_ERR_NEED_MORE_IMGS:
            print("Reason: Need more images or less overlap.")
        elif status == cv2.Stitcher_ERR_HOMOGRAPHY_EST_FAIL:
            print("Reason: Homography estimation failed (not enough matching features).")
        elif status == cv2.Stitcher_ERR_CAMERA_PARAMS_ADJUST_FAIL:
            print("Reason: Camera parameters adjustment failed.")
extracted_frames_folder = r"C:\Users\adila\Videos\Captures\ExtractedFrames"
output_stitched_path = r"C:\Users\adila\Videos\Captures\stitched_drone_footage.png"
stitch_images_with_opencv(extracted_frames_folder, output_stitched_path)
import folium
from folium.raster_layers import ImageOverlay
import os
def overlay_image_on_folium_map(stitched_image_path, bounds, output_html_path="map_overlay.html", center_coords=None):

    if not os.path.exists(stitched_image_path):
        print(f"Error: Stitched image not found at {stitched_image_path}")
        return

    if center_coords is None:
        lat_min, lon_min = bounds[0][0], bounds[0][1] 
        lat_max, lon_max = bounds[1][0], bounds[1][1] 
        center_lat = (lat_min + lat_max) / 2
        center_lon = (lon_min + lon_max) / 2
        center_coords = [center_lat, center_lon]

    m = folium.Map(location=center_coords, zoom_start=15, tiles="OpenStreetMap") 
    image_overlay = ImageOverlay(
        image=stitched_image_path,
        bounds=bounds,
        opacity=0.8,
        alt="Stitched Drone Footage"
    ).add_to(m)

    folium.Marker(
        location=center_coords,
        popup=f"Center of Stitched Image: {center_coords[0]:.4f}, {center_coords[1]:.4f}",
        icon=folium.Icon(color='red')
    ).add_to(m)

    # Save the map to an HTML file
    m.save(output_html_path)
    print(f"Folium map saved to {output_html_path}")
    print(f"Stitched image bounds used: {bounds}")
    print(f"Map centered at: {center_coords}")
stitched_image_file = r"C:\Users\adila\Videos\Captures\MyStitchedDroneImage.png"
image_bounds = [
    [30.1100, 78.2800],
    [30.1200, 78.2900]
]

map_center_coordinates = [30.1158, 78.2853]
output_map_html = "drone_footage_overlay_map.html"

# Call the function
overlay_image_on_folium_map(
    stitched_image_path=stitched_image_file,
    bounds=image_bounds,
    output_html_path=output_map_html,
    center_coords=map_center_coordinates
)

print(f"\nInteractive map saved to: {os.path.abspath(output_map_html)}")
print("Open this HTML file in a web browser.")
