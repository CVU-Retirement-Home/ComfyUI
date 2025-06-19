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
tested = ["As a reporter standing at the edge of what was once a thriving coastal city, I see nothing but devastation. The streets are now vast, murky rivers, with water levels rising well past the second floor of nearby buildings. Cars are half-submerged, their metal frames twisted and barely recognizable. Floating debris, broken pieces of homes, and uprooted trees are scattered across the flooded streets. In the distance, a once-bustling pier is now reduced to rubble, with remnants of boats and docks floating aimlessly. Survivors, faces filled with exhaustion and disbelief, wade through the water, looking for missing family members or trying to salvage anything left behind. The sky above is thick with dark clouds, casting an eerie shadow over the scene. The silence of the water is broken only by the occasional distant crash of more debris. The power of the tsunami is palpable here—what was once a vibrant community now lies in ruin.", "A wide-angle view from a reporter's perspective, showing a flooded town after a tsunami. In the foreground, the reporter stands on a debris-covered street, holding a camera, documenting the scene. The water has receded, leaving behind ruined homes, cars stuck in mud, and fallen electrical poles. The mood is somber, and the reporter's expression conveys a mixture of disbelief and professionalism.","A reporter stands in front of a massive landslide that has covered a road and buried homes. The reporter is equipped with safety gear and a microphone, documenting the aftermath. In the background, the landslide has caused devastation, with mud and rocks scattered over the area. The sky is cloudy, and emergency responders are digging through the debris in search of survivors. The scale of the landslide is overwhelming.","A reporter walks through a barren landscape affected by severe drought. Once-thriving farmlands are now cracked and dry, with wilting crops and empty water reservoirs. The reporter, holding a microphone, looks out at the desolate scene. The sky is clear, but the air is hot and dry. In the distance, you can see livestock struggling and water trucks driving through the cracked earth to deliver what little water remains."]

def main():
    #CONFIGS
    image_to_generate_count = 50 #how many images to generate
    neg_prompt = '(deformed iris, deformed pupils, semi-realistic, cgi, 3d, render, sketch, cartoon, drawing, anime, mutated hands and fingers:1.4), (deformed, distorted, disfigured:1.3), poorly drawn, bad anatomy, wrong anatomy, extra limb, missing limb, floating limbs, disconnected limbs, mutation, mutated, ugly, disgusting, amputation, UnrealisticDream'
    
    pos_prompt = ["A rural neighborhood destroyed by a tornado. Uprooted trees and shattered homes line the background. Firefighters and paramedics, some with dirt and debris on their uniforms, search for survivors. ","Wide lens view of a cracked and damaged streets of a city after a major earthquake. Buildings are toppled, some reduced to rubble, and others have large cracks running through them. The reporter holds a microphone and speaks with urgency while surveying the destruction. The air is thick with dust, and emergency teams are seen searching for survivors. The reporter's expression is one of disbelief, the sky is clear but hazy from the dust.","A reporter stands amidst the devastation of a coastal city hit by a powerful hurricane. The streets are flooded with debris, and damaged buildings are partially submerged in water. The reporter is soaked, holding a microphone and wearing a rain jacket. The sky is still dark with clouds, and strong winds are causing debris to fly. In the background, rescue teams and helicopters hover over the city, performing search and rescue operations.","A dense city street reduced to chaos after a major earthquake. Entire buildings have collapsed into piles of broken concrete and rebar. First responders in high-visibility gear and helmets are crawling over rubble, using rescue dogs and listening devices to search for trapped survivors. A firefighter carries a dust-covered child out of the debris, while a paramedic tends to an injured elderly man on a stretcher nearby. A news reporter in a hard hat stands at a safe distance, narrating the scene, her face streaked with dust.","The city is cloaked in darkness, power knocked out by a massive earthquake. Portable floodlights cast harsh beams across the wreckage. Search-and-rescue teams in reflective gear move fast among collapsed buildings. Emergency workers shout over walkie-talkies, guiding stretchers to ambulances. A news reporter with a flashlight clipped to their vest speaks into the camera, voice steady despite the chaos, while behind them, rescuers pull someone from the rubble—everyone coated in a layer of dust and debris.","In a suburban neighborhood devastated by an earthquake, homes have crumbled and power lines are down. First responders coordinate rescue efforts while local residents assist. Firefighters use pry bars to lift beams, while medics, covered in ash and sweat, perform first aid. Civilians, faces gray with dust, offer water and blankets. A newscaster stands beside a rescue tent, mud on their boots, reporting live as a helicopter circles overhead.",""]
    
    model_settings_prompt =  'RAW photo, dslr, soft lighting, film grain, Fujifilm XT3' #'masterpiece, 4k, ray tracing, intricate details, highly-detailed, hyper-realistic, 8k RAW Editorial Photo,film grain ISO 200 faded film, 35mm photo, grainy, vignette, vintage, Kodachrome, Lomography, stained, highly detailed, found footage'
    lora_name = "epiCRealismHelper.safetensors" #copy filename from \models\loras with extension
    ckpt_path = "realisticVisionV60B1_v51HyperVAE.safetensors" #base model
    output_folder = r'D:\SeeThrough\ComfyUI_windows_portable\ComfyUI\retirement_dataset_fake_realistic6_04062025' #folder to save generate images to, defaults to output folder in root comfyui
    upscale_model = '4x-UltraSharp.pth'
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


        cliptextencode = NODE_CLASS_MAPPINGS["CLIPTextEncode"]()
        cliptextencode_7 = cliptextencode.encode(
            text=neg_prompt,
            clip=get_value_at_index(checkpointloadersimple_4, 1),
        )
        
        upscalemodelloader = NODE_CLASS_MAPPINGS["UpscaleModelLoader"]()
        upscalemodelloader_32 = upscalemodelloader.load_model(
            model_name=upscale_model
        )
        for idx,prompt in enumerate(pos_prompt):
            cliptextencode_16 = cliptextencode.encode(
                text=prompt+model_settings_prompt,
                clip=get_value_at_index(checkpointloadersimple_4, 1),
            )

            saveimage = NODE_CLASS_MAPPINGS["SaveImage"]()

            for q in range(image_to_generate_count):
                ksampler = NODE_CLASS_MAPPINGS["KSampler"]()
                ksampler_3 = ksampler.sample(
                    seed=random.randint(1, 2**64),
                    steps=7,
                    cfg=2.5,
                    sampler_name="dpmpp_2m_sde",
                    scheduler="karras",
                    denoise=1,
                    model=get_value_at_index(checkpointloadersimple_4, 0),
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

                imagescale = NODE_CLASS_MAPPINGS["ImageScaleBy"]()
                imagescale_46 = imagescale.upscale(
                    upscale_method="area",
                    scale_by = 1.5,
                    image=get_value_at_index(imageupscalewithmodel_45, 0),
                )

                vaeencode = NODE_CLASS_MAPPINGS["VAEEncode"]()
                vaeencode_47 = vaeencode.encode(
                    pixels=get_value_at_index(imagescale_46, 0),
                    vae=get_value_at_index(checkpointloadersimple_4, 2),
                )

                ksampler_48 = ksampler.sample(
                    seed=random.randint(1, 2**64),
                    steps=7,
                    cfg=6,
                    sampler_name="dpmpp_2m_sde",
                    scheduler="karras",
                    denoise=0.35,
                    model=get_value_at_index(checkpointloadersimple_4, 0),
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

                thread = threading.Thread(target=saveimage.save_images, kwargs= {'filename_prefix' : "img_encoded", 'count' : f'{q}_{idx}','output_folder' : output_folder, 'images' :get_value_at_index(vaedecode_49, 0)})
                thread.start()
                


if __name__ == "__main__":
    main()
