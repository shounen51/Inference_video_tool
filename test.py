import timm
import time
try:
    action_model = timm.create_model("wide_resnet50_2",checkpoint_path="weight/action_3IR_Wresnet50.pth", num_classes = 3).eval()
    print("B")
    action_model.cuda()
    print("C")
except Exception as e:
    print("D")
    print(e)
time.sleep(3)
print("A")