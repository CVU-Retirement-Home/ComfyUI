import os
import random
import sys
from typing import Sequence, Mapping, Any, Union
import torch
import threading


def get_value_at_index(obj: Union[Sequence, Mapping], index: int) -> Any:
    """Returns the value at the given index of a sequence or mapping.

    If the object is a sequence (like list or string), returns the value at the given index.
    If the object is a mapping (like a dictionary), returns the value at the index-th key.

    Some return a dictionary, in these cases, we look for the "results" key

    Args:
        obj (Union[Sequence, Mapping]): The object to retrieve the value from.
        index (int): The index of the value to retrieve.

    Returns:
        Any: The value at the given index.

    Raises:
        IndexError: If the index is out of bounds for the object and the object is not a mapping.
    """
    try:
        #print(obj,index)
        return obj[index]
    except KeyError:
        return obj["result"][index]


def find_path(name: str, path: str = None) -> str:
    """
    Recursively looks at parent folders starting from the given path until it finds the given name.
    Returns the path as a Path object if found, or None otherwise.
    """
    # If no path is given, use the current working directory
    if path is None:
        path = os.getcwd()

    # Check if the current directory contains the name
    if name in os.listdir(path):
        path_name = os.path.join(path, name)
        print(f"{name} found: {path_name}")
        return path_name

    # Get the parent directory
    parent_directory = os.path.dirname(path)

    # If the parent directory is the same as the current directory, we've reached the root and stop the search
    if parent_directory == path:
        return None

    # Recursively call the function with the parent directory
    return find_path(name, parent_directory)


def add_comfyui_directory_to_sys_path() -> None:
    """
    Add 'ComfyUI' to the sys.path
    """
    comfyui_path = find_path("ComfyUI")
    if comfyui_path is not None and os.path.isdir(comfyui_path):
        sys.path.append(comfyui_path)
        print(f"'{comfyui_path}' added to sys.path")


def add_extra_model_paths() -> None:
    """
    Parse the optional extra_model_paths.yaml file and add the parsed paths to the sys.path.
    """
    try:
        from main import load_extra_path_config
    except ImportError:
        print(
            "Could not import load_extra_path_config from main.py. Looking in utils.extra_config instead."
        )
        from utils.extra_config import load_extra_path_config

    extra_model_paths = find_path("extra_model_paths.yaml")

    if extra_model_paths is not None:
        load_extra_path_config(extra_model_paths)
    else:
        print("Could not find the extra_model_paths config file.")


add_comfyui_directory_to_sys_path()
add_extra_model_paths()


def import_custom_nodes() -> None:
    """Find all custom nodes in the custom_nodes folder and add those node objects to NODE_CLASS_MAPPINGS

    This function sets up a new asyncio event loop, initializes the PromptServer,
    creates a PromptQueue, and initializes the custom nodes.
    """
    import asyncio
    import execution
    import server

    # Creating a new event loop and setting it as the default loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # Creating an instance of PromptServer with the loop
    server_instance = server.PromptServer(loop)
    execution.PromptQueue(server_instance)


from nodes import NODE_CLASS_MAPPINGS


def main():
    #CONFIGS
    image_to_generate_count = 50 #how many images to generate
    neg_prompt = "painting, drawing, sketch, cartoon, anime, manga, render, CG, 3d, watermark, signature, label, uneven lines, blurry, low-res, artifacts, distorted, bad anatomy, unrealistic lighting, jpeg artifacts, lowres, oversaturated"
    
    pos_prompt = ["A highly realistic image of a vibrant coastal neighborhood after a powerful hurricane. One two-story beach house is dramatically tilted, its foundation visibly collapsed and concrete supports shattered. The adjacent single-story house shows partial damage but remains standing. Debris, broken wood, and scattered rubble litter the sandy ground. The sky is overcast, suggesting recent storm activity.","A hyper-realistic aerial view of a massive landslide cutting through a densely forested mountain. A large swath of earth has collapsed, leaving a wide, barren scar across the hillside where trees have been violently stripped away. The slide path is filled with mud, rocks, and uprooted trees, forming a chaotic, jagged trail that extends down into a valley. Surrounding the destruction, untouched green conifer forests contrast sharply with the brown and gray debris. Mist and low clouds hover over the distant hills, enhancing the somber, post-disaster atmosphere. The lighting is natural, overcast,reflecting the aftermath of a geological catastrophe.","A highly realistic ground-level view of a recent landslide in a forested mountain area. The muddy, debris-strewn path is littered with large boulders, broken branches, and freshly fallen tree trunks—some stacked chaotically, others partially buried in wet earth. The surrounding dense forest, with dark green foliage and towering trees, frames the destruction. Mist hangs in the air, suggesting recent rainfall and adding a damp, heavy atmosphere to the scene. The ground is slick with mud and shallow water flows across it, reflecting the overcast sky.","A realistic landslide scene on a mountain forest road, where a large section of the asphalt road has collapsed into a deep, muddy slope. The metal guardrails are bent and hanging, supported weakly by wooden braces. The road is surrounded by dense, green, tropical forest with tall ferns and trees. Traffic cones line the undamaged section of the road, and the sky is overcast,  Capture the raw aftermath of the landslide with high detail, emphasizing the scale of erosion and road damage.","A realistic aerial view of a suburban neighborhood severely impacted by a hurricane. Streets are heavily flooded with murky water, and multiple vehicles attempt to drive through the submerged roads, creating ripples and wakes. Large fallen trees and debris block intersections, and power lines hang low or are entangled in the branches. A few parked cars are partially submerged near buildings. The surrounding area shows signs of wind damage, with palm trees bent and scattered branches everywhere.","wide lens view of a post-disaster urban scene, collapsed buildings, destroyed infrastructure, debris-strewn streets, dusty atmosphere, raw devastation, cinematic realism, emergency response, photojournalistic detail, grain, motionblur","A top-down aerial photo of a flooded town. Brown, muddy water covers streets and parts of houses. Buildings are partially destroyed, with debris floating and scattered throughout the scene. Some rooftops remain intact, but the area shows widespread devastation.",'A heartbreaking aerial view of a town swallowed by floodwaters. Homes are ripped apart, their contents spilling into muddy currents. The streets are unrecognizable rivers of destruction, and the wreckage tells a silent story of loss and survival.','a massive landslide in a mountainous rural area, soil and debris sliding down a hill, destroyed trees and rocks, collapsed road or partially buried houses, heavy overcast sky, wet soil textures, realistic mud and erosion patterns,','a suburban house partially submerged in muddy flood water, realistic reflections on the water surface, cloudy overcast sky, dense pine forest in the background, waterlogged yard,']
    
    model_settings_prompt =  "natural shadow and lighting, 8k, uhd"
 #'masterpiece, 4k, ray tracing, intricate details, highly-detailed, hyper-realistic, 8k RAW Editorial Photo,film grain ISO 200 faded film, 35mm photo, grainy, vignette, vintage, Kodachrome, Lomography, stained, highly detailed, found footage'
    lora_name = "epiCRealismHelper.safetensors" #copy filename from \models\loras with extension
    ckpt_path = "realvisxlV40_v40LightningBakedvae.safetensors" #base model
    output_folder = r'D:\SeeThrough\ComfyUI_windows_portable\ComfyUI\retirement_dataset_fake_realistic6_05022025_3' #folder to save generate images to, defaults to output folder in root comfyui
    image_template_path = [r"D:\SCVU\deepfake_dataset\disaster_images\hurricane_destruction\keep\hurricane_destruction_214.jpg",r"D:\SCVU\deepfake_dataset\disaster_images\landslide_photo\keep\landslide_photo_039.jpg",r"D:\SCVU\deepfake_dataset\disaster_images\landslide_photo\keep\landslide_photo_116.jpg",
    r"D:\SCVU\deepfake_dataset\disaster_images\landslide_photo\keep\landslide_photo_118.jpg",
    r"D:\SCVU\deepfake_dataset\disaster_images\hurricane_destruction\keep\hurricane_destruction_297.jpg",
    r"D:\SCVU\deepfake_dataset\disaster_images\natural_disaster_scene\keep\natural_disaster_scene_599.jpg",r"D:\SCVU\deepfake_dataset\disaster_images\natural_disaster_scene\keep\natural_disaster_scene_255.jpg",r"D:\SCVU\deepfake_dataset\disaster_images\landslide_photo\keep\landslide_photo_261.jpg",r"D:\SCVU\deepfake_dataset\disaster_images\natural_disaster_scene\keep\natural_disaster_scene_500.jpg"]
    upscale_model = '4x_NMKD-Superscale-SP_178000_G.pth'
    filename_template ='img2img_refiner'
    control_net_name = "control-lora-canny-rank256.safetensors"
    refiner = "sd_xl_refiner_1.0.safetensors"
    vae_name = 'sdxl_vae.safetensors'
    os.makedirs(output_folder,exist_ok=True)


    #workflow code
    #able to adjust the paramters manually here but for do it on the UI to test if the params actualyl work
    with torch.inference_mode():
        checkpointloadersimple = NODE_CLASS_MAPPINGS["CheckpointLoaderSimple"]()
        checkpointloadersimple_4 = checkpointloadersimple.load_checkpoint(
            ckpt_name= ckpt_path
        )

        emptylatentimage = NODE_CLASS_MAPPINGS["EmptyLatentImage"]()
        emptylatentimage_5 = emptylatentimage.generate(
            width=1152, height=896, batch_size=1
        )
        
        clipsetlastlayer = NODE_CLASS_MAPPINGS["CLIPSetLastLayer"]()
        clipsetlastlayer_74 = clipsetlastlayer.set_last_layer(
            stop_at_clip_layer=-23, clip=get_value_at_index(checkpointloadersimple_4, 1)
        )
        cliptextencode = NODE_CLASS_MAPPINGS["CLIPTextEncode"]()
        cliptextencode_7 = cliptextencode.encode(
            text=neg_prompt,
            clip=get_value_at_index(clipsetlastlayer_74, 0),
        )
        
        upscalemodelloader = NODE_CLASS_MAPPINGS["UpscaleModelLoader"]()
        upscalemodelloader_32 = upscalemodelloader.load_model(
            model_name=upscale_model
        )
        
        controlnetloader = NODE_CLASS_MAPPINGS["ControlNetLoader"]()
        controlnetloader_54 = controlnetloader.load_controlnet(
            control_net_name=control_net_name
        )
        
        checkpointloadersimple_78 = checkpointloadersimple.load_checkpoint(
            ckpt_name=refiner
        )
        cliptextencode_82 = cliptextencode.encode(
            text=neg_prompt,
            clip=get_value_at_index(checkpointloadersimple_78, 1),
        )


       
        vaeloader = NODE_CLASS_MAPPINGS["VAELoader"]()
        vaeloader_87 = vaeloader.load_vae(vae_name=vae_name)
        canny = NODE_CLASS_MAPPINGS["Canny"]()
        controlnetapplyadvanced = NODE_CLASS_MAPPINGS["ControlNetApplyAdvanced"]()
        ksampler = NODE_CLASS_MAPPINGS["KSampler"]()
        vaedecode = NODE_CLASS_MAPPINGS["VAEDecode"]()
        imageupscalewithmodel = NODE_CLASS_MAPPINGS["ImageUpscaleWithModel"]()
        imagescaleby = NODE_CLASS_MAPPINGS["ImageScaleBy"]()

        for idx,prompt in enumerate(pos_prompt):
            loadimage = NODE_CLASS_MAPPINGS["LoadImage"]()
            loadimage_55 = loadimage.load_image(image=image_template_path[idx])

            canny = NODE_CLASS_MAPPINGS["Canny"]()
            canny_59 = canny.detect_edge(
                low_threshold=0.2,
                high_threshold=0.9,
                image=get_value_at_index(loadimage_55, 0),
            )
        
            cliptextencode_16 = cliptextencode.encode(
                text=prompt+model_settings_prompt,
                clip=get_value_at_index(clipsetlastlayer_74, 0),
            )

            cliptextencode_83 = cliptextencode.encode(
                text=prompt+model_settings_prompt,
                clip=get_value_at_index(checkpointloadersimple_78, 1),
        )

            controlnetapplyadvanced_57 = controlnetapplyadvanced.apply_controlnet(
                strength=1,
                start_percent=0,
                end_percent=1,
                positive=get_value_at_index(cliptextencode_16, 0),
                negative=get_value_at_index(cliptextencode_7, 0),
                control_net=get_value_at_index(controlnetloader_54, 0),
                image=get_value_at_index(canny_59, 0),
            )
            for q in range(image_to_generate_count):
                ksampler_3 = ksampler.sample(
                    seed=random.randint(1, 2**64),
                    steps=80,
                    cfg=6,
                    sampler_name="dpmpp_2m_sde",
                    scheduler="karras",
                    denoise=1,
                    model=get_value_at_index(checkpointloadersimple_4, 0),
                    positive=get_value_at_index(controlnetapplyadvanced_57, 0),
                    negative=get_value_at_index(controlnetapplyadvanced_57, 1),
                    latent_image=get_value_at_index(emptylatentimage_5, 0),
                )

                ksampler_84 = ksampler.sample(
                    seed=random.randint(1, 2**64),
                    steps=20,
                    cfg=7,
                    sampler_name="dpmpp_2m_sde",
                    scheduler="normal",
                    denoise=0.2,
                    model=get_value_at_index(checkpointloadersimple_78, 0),
                    positive=get_value_at_index(cliptextencode_83, 0),
                    negative=get_value_at_index(cliptextencode_82, 0),
                    latent_image=get_value_at_index(ksampler_3, 0),
                )

                vaedecode_85 = vaedecode.decode(
                    samples=get_value_at_index(ksampler_84, 0),
                    vae=get_value_at_index(vaeloader_87, 0),
                )

                imageupscalewithmodel_45 = imageupscalewithmodel.upscale(
                    upscale_model=get_value_at_index(upscalemodelloader_32, 0),
                    image=get_value_at_index(vaedecode_85, 0),
                )

                imagescaleby_64 = imagescaleby.upscale(
                    upscale_method="area",
                    scale_by=1.100000000000000,
                    image=get_value_at_index(imageupscalewithmodel_45, 0),
                )
                saveimage = NODE_CLASS_MAPPINGS["SaveImage"]()
                thread = threading.Thread(target=saveimage.save_images, kwargs= {'filename_prefix' : filename_template, 'count' : f'{q}_{idx}','output_folder' : output_folder, 'images' :get_value_at_index(imagescaleby_64, 0)})
                thread.start()
                
if __name__ == "__main__":
    main()
