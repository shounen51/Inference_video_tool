from configs import NAS_path, video_type

LINE_try_exit_title = "King exit"
LINE_try_exit = "Are you sure about that?"

LINE_checking_weight = "\nFinding weight to update...\n"
LINE_NO_weight_found = f"Your models are the newest... Or AIE forgot to upload.\n"

LINE_force_run = "\nForce mode enable. Skip checking GPU.\n"
LINE_checking_GPU = "\nChecking GPU status...\n"
LINE_GPU_busy = "Seems This GPU is busy now. Try later or contact AIE leader.\n"
LINE_GPU_ready = "Nobody is using this GPU. It's yours now.\n"

LINE_checking_video = "\nPreparing videos to run...\n"
LINE_NO_video_found = f"No video or image in 250_NAS/video2/AIE_run_video/video.\nPlease check your file is : {', '.join(video_type)}\n"

LINE_run_start = "\nStart running your videos...\n"
LINE_find_no_weight = "\nThere is no model for this fonction. Please contact AIE leader.\n"
LINE_run_end = "Running is over.\n"

LINE_end = "done.\n"
