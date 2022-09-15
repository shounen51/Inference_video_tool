video_path = "./video/"
weight_path = "./weight/"
NAS_path = "/mnt/250/DemoVideo2/AIE_run_video/video/"
NAS_output = "/mnt/250/DemoVideo2/AIE_run_video/result/"
NAS_weight_path = "/mnt/250/DemoVideo2/AIE_run_video/weight/"
video_type = ['mp4','avi','mkv','jpg','jpeg','png']
wight_type = ['pt', 'pth', 'tar']

functions = {
    "action":"python3 /home/ubuntu/work/yolov5_ori/detect_action_4auto.py",
    "wheelchair":""
}
args = {
    "action":{
        "--weights1":"",
        "--weights2":"",
        "--source": "",
        "--act-model":"wide_resnet50_2",
        "--conf-thres":0.4,
        "--hide-labels":"",
        "--hide-conf":""
        },
    "wheelchair":""
}