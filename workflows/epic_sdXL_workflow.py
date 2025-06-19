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
    neg_prompt = "cartoon, cgi, render, illustration, painting, drawing,bad proportions, low resolution, bad, ugly, bad hands, bad teeth, terrible, painting, 3d, comic, anime, manga, unrealistic, watermark, signature, worst quality, low quality,missing limbs, disfigured"
    
    pos_prompt = ["Generate a hyper-realistic image of a post-earthquake and tsunami disaster scene in Southeast Asia. Maintain the muddy, debris-covered ground and the damaged buildings in the background. a few emergency personnel in safety gear assessing the area, and distressed civilians in the mid-ground searching for belongings. Show cracked roads, fallen streetlights, and scattered personal items like clothes and furniture. reflecting a somber, early morning atmosphere after the disaster struck.","Wide-angle photo of the aftermath of a volcanic eruption, ash-covered town, collapsed structures, people wearing masks walking through gray haze, scattered debris, smoldering ground, distant silhouette of the volcano with light smoke, golden-hour lighting, somber tone, 4K resolution, documentary style, aerial drone shot",'On-ground photo of a recent landslide in a rural village in Northern Thailand, muddy terrain engulfing wooden homes, villagers clearing debris, emergency personnel with helmets and reflective vests, broken trees, heavy clouds and fog in the background, realistic lighting and textures, muted color palette, Nikon D850 lens simulation, sharp depth of field, disaster reportage style','Street-level image of the aftermath of a tropical storm in Manila, downed electric poles, flooded roads, palm trees bent from high winds, locals wading through waist-high water, makeshift rafts carrying supplies, military trucks delivering aid, gloomy skies, realistic water reflections, raw documentary tone, captured in stormy lighting conditions, photojournalistic lens','High-angle shot of a massive forest fire in Kalimantan, Indonesia, thick smoke clouds rising from burning rainforest, orange flames visible in tree canopy, scorched earth patterns below, helicopters dropping water from above, blurred haze in the background, sunset lighting with a warm orange glow, Canon EOS drone shot, environmental documentary aesthetic','Rural Myanmar after a Category 4 cyclone, drone view of shattered huts and torn-up trees, muddy roads strewn with debris, humanitarian aid tents set up in open fields, people in wet clothes receiving supplies, UN workers in light blue vests distributing food packages, distant mountains under gray skies, cinematic tone, Canon 5D Mark IV, news coverage realism','Aerial perspective of widespread forest fire aftermath in Borneo, Indonesia, scorched land and blackened trees stretching across the landscape, small teams of fire crews spraying hotspots, haze-filled air with orange-tinted sunlight, satellite uplink truck and news reporters wearing masks, drones flying overhead, cinematic composition, drone shot, realistic depth and shadows','Beachfront village in southern Thailand devastated by tsunami, debris scattered across wet sand, collapsed homes, rescue workers in red gear moving through wreckage, crying locals searching through ruins, helicopters hovering above with emergency teams dropping supplies, somber mood, real camera optics, Sony Alpha 1 with 50mm lens, photojournalistic detail, realism-focused deepfake tone','Indoor shelter in Malaysia during typhoon emergency, gymnasium filled with evacuees lying on mats, families grouped together under dim fluorescent lights, Red Crescent medical staff attending to patients, blurred background showing emergency supply boxes, handheld DSLR composition, Canon lens realism, 4K cinematic news look','Street-level photograph illustrating the extreme heatwave in Bangkok, Thailand; pedestrians seeking shade under umbrellas; heat haze visible above asphalt roads; digital temperature display showing 43°C; emergency medical personnel attending to heatstroke victims; bright sunlight casting harsh shadows; captured with a Fujifilm X-T4, 23mm lens, f/2 aperture; high-contrast lighting, vivid colors, photorealistic detail.','Image capturing the impact of flash floods in Sumatra, Indonesia; muddy waters engulfing homes and streets; residents using makeshift rafts for transportation; fallen trees and debris scattered throughout; cloudy skies with intermittent rain; shot with a Sony Alpha 7R IV, 28mm lens, f/3.5 aperture; realistic lighting, high-detail rendering, true-to-life colors.','Photograph showing the devastation caused by a landslide in Davao de Oro, Philippines; collapsed structures buried under mud and debris; rescue teams searching for survivors amidst the rubble; somber expressions on faces of displaced residents; overcast weather contributing to a gloomy atmosphere; taken with a Nikon D850, 50mm lens, f/5.6 aperture; documentary-style composition, sharp focus, natural color grading.','Aerial drone image capturing the aftermath of a powerful tornado in the Midwest United States; flattened homes, uprooted trees, and debris scattered across the landscape; emergency responders searching through rubble; overcast skies with lingering storm clouds; shot with a DJI Mavic 3 drone, 24mm lens, f/2.8 aperture; photorealistic, cinematic lighting, high dynamic range.','Image depicting the devastation caused by monsoon floods in India and Pakistan; homes submerged under water, people stranded on rooftops awaiting rescue; boats navigating through flooded streets; overcast weather contributing to a gloomy atmosphere; shot with a Fujifilm X-T4, 23mm lens, f/2 aperture; high-contrast lighting, vivid colors, photorealistic detail.']
    
    model_settings_prompt =  'Taken from a news report point of view, imperfect lighting, “atural photo flaws,4k, ray tracing, intricate details, highly-detailed, hyper-realistic, 8k RAW Editorial Photo,film grain ISO 200 faded film, 35mm photo, grainy, vignette, vintage, Kodachrome, Lomography, stained, highly detailed, found footage'
    lora_name = "epicNewPhoto.safetensors" #copy filename from \models\loras with extension
    ckpt_path = "epicrealismXL_vxviLastfameRealism.safetensors" #base model
    output_folder = r'D:\SeeThrough\ComfyUI_windows_portable\ComfyUI\retirement_dataset_fake_04252025' #folder to save generate images to, defaults to output folder in root comfyui
    upscale_model = 'RealESRGAN_x8.pth' #upsacle_model
    filename_template = 'epic_sdXL' #prefix for filename eg sd_xl_0_0.jpg
    os.makedirs(output_folder,exist_ok=True)

    
    with torch.inference_mode():
        checkpointloadersimple = NODE_CLASS_MAPPINGS["CheckpointLoaderSimple"]()
        checkpointloadersimple_4 = checkpointloadersimple.load_checkpoint(
            ckpt_name= ckpt_path
        )

        emptylatentimage = NODE_CLASS_MAPPINGS["EmptyLatentImage"]()
        emptylatentimage_5 = emptylatentimage.generate(
            width=768, height=512, batch_size=1
        )

        loraloader = NODE_CLASS_MAPPINGS["LoraLoader"]()
        loraloader_43 = loraloader.load_lora(
            lora_name=lora_name,
            strength_model=0.8,
            strength_clip=1,
            model=get_value_at_index(checkpointloadersimple_4, 0),
            clip=get_value_at_index(checkpointloadersimple_4, 1),
        )

        cliptextencode = NODE_CLASS_MAPPINGS["CLIPTextEncode"]()
        cliptextencode_7 = cliptextencode.encode(
            text=neg_prompt,
            clip=get_value_at_index(loraloader_43, 1),
        )
        
        upscalemodelloader = NODE_CLASS_MAPPINGS["UpscaleModelLoader"]()
        upscalemodelloader_32 = upscalemodelloader.load_model(
            model_name=upscale_model
        )
        for idx,prompt in enumerate(pos_prompt):
            cliptextencode_16 = cliptextencode.encode(
                text=prompt+model_settings_prompt,
                clip=get_value_at_index(loraloader_43, 1),
            )

            saveimage = NODE_CLASS_MAPPINGS["SaveImage"]()

            for q in range(image_to_generate_count):
                ksampler = NODE_CLASS_MAPPINGS["KSampler"]()
                ksampler_3 = ksampler.sample(
                    seed=random.randint(1, 2**64),
                    steps=30,
                    cfg=8,
                    sampler_name="dpmpp_2m_sde",
                    scheduler="karras",
                    denoise=1,
                    model=get_value_at_index(loraloader_43, 0),
                    positive=get_value_at_index(cliptextencode_16, 0),
                    negative=get_value_at_index(cliptextencode_7, 0),
                    latent_image=get_value_at_index(emptylatentimage_5, 0),
                )

                vaedecode = NODE_CLASS_MAPPINGS["VAEDecode"]()
                vaedecode_8 = vaedecode.decode(
                    samples=get_value_at_index(ksampler_3, 0),
                    vae=get_value_at_index(checkpointloadersimple_4, 2),
                )

                imageupscalewithmodel = NODE_CLASS_MAPPINGS["ImageUpscaleWithModel"]()
                imageupscalewithmodel_45 = imageupscalewithmodel.upscale(
                    upscale_model=get_value_at_index(upscalemodelloader_32, 0),
                    image=get_value_at_index(vaedecode_8, 0),
                )

                imagescale = NODE_CLASS_MAPPINGS["ImageScale"]()
                imagescale_46 = imagescale.upscale(
                    upscale_method="area",
                    width= 768*2,
                    height= 1024,
                    crop="disabled",
                    image=get_value_at_index(imageupscalewithmodel_45, 0),
                )

                vaeencode = NODE_CLASS_MAPPINGS["VAEEncode"]()
                vaeencode_47 = vaeencode.encode(
                    pixels=get_value_at_index(imagescale_46, 0),
                    vae=get_value_at_index(checkpointloadersimple_4, 2),
                )

                ksampler_48 = ksampler.sample(
                    seed=random.randint(1, 2**64),
                    steps=30,
                    cfg=8,
                    sampler_name="dpmpp_2m_sde",
                    scheduler="karras",
                    denoise=0.3,
                    model=get_value_at_index(loraloader_43, 0),
                    positive=get_value_at_index(cliptextencode_16, 0),
                    negative=get_value_at_index(cliptextencode_7, 0),
                    latent_image=get_value_at_index(vaeencode_47, 0),
                )

                vaedecode_49 = vaedecode.decode(
                    samples=get_value_at_index(ksampler_48, 0),
                    vae=get_value_at_index(checkpointloadersimple_4, 2),
                )
                
                def save_image(filename_prefix,count,output_folder,image):
                    print('saving image in thread')
                    saveimage.save_images(
                    filename_prefix=filename_prefix,
                    count = count,
                    output_folder = output_folder,
                    images=image,
                )

                thread = threading.Thread(target=saveimage.save_images, kwargs= {'filename_prefix' : filename_template, 'count' : f'{q}_{idx}','output_folder' : output_folder, 'images' :get_value_at_index(vaedecode_49, 0)})
                thread.start()
                


if __name__ == "__main__":
    main()
