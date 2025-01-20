# 视频章节数据如下:
# 00:00:00 00:02:50 Introduction_and_Welcome
# 00:02:50 00:13:07 K8s_Security_Best_Practices
# 00:13:07 00:35:49 Create_your_course_K8s_cluster
# 00:35:49 00:38:02 Crictl_instead_of_Docker
# 00:38:02 00:57:27 Foundation_Kubernetes_Secure_Architecture
# 00:57:27 01:18:12 Foundation_Containers_under_the_hood
# 01:18:12 01:18:53 Cluster_Reset
# 01:18:53 01:46:54 Cluster_Setup_Network_Policies
# 01:46:54 02:02:06 Cluster_Setup_GUI_Elements
# 02:02:06 02:02:48 K8s_Docs_Version
# 02:02:48 02:23:54 Cluster_Setup_Secure_Ingress
# 02:23:54 02:34:13 Cluster_Setup_Node_Metadata_Protection
# 02:34:13 02:47:47 Cluster_Setup_CIS_Benchmarks
# 02:47:47 02:58:23 Cluster_Setup_Verify_Platform_Binaries
# 02:58:23 03:31:26 Cluster_Hardening_RBAC
# 03:31:26 03:49:06 Cluster_Hardening_Exercise_caution_in_using_ServiceAccounts
# 03:49:06 04:17:25 Cluster_Hardening_Restrict_API_Access
# 04:17:25 04:38:59 Cluster_Hardening_Upgrade_Kubernetes
# 04:38:59 05:26:44 Microservice_Vulnerabilities_Manage_Kubernetes_Secrets
# 05:26:44 05:55:19 Microservice_Vulnerabilities_Container_Runtime_Sandboxes
# 05:55:19 06:12:01 Microservice_Vulnerabilities_OS_Level_Security_Domains
# 06:12:01 06:27:12 Microservice_Vulnerabilities_mTLS
# 06:27:12 06:27:54 Cluster_Reset
# 06:27:54 07:07:33 Open_Policy_Agent_OPA
# 07:07:33 07:29:37 Supply_Chain_Security_Image_Footprint
# 07:29:37 07:52:39 Supply_Chain_Security_Static_Analysis
# 07:52:39 08:06:26 Supply_Chain_Security_Image_Vulnerability_Scanning
# 08:06:26 08:32:01 Supply_Chain_Security_Secure_Supply_Chain
# 08:32:01 09:16:36 Runtime_Security_Behavioral_Analytics_at_host_and_container_level
# 09:16:36 09:34:24 Runtime_Security_Immutability_of_containers_at_runtime
# 09:34:24 10:06:46 Runtime_Security_Auditing
# 10:06:46 10:45:41 System_Hardening_Kernel_Hardening_Tools
# 10:45:41 11:05:20 System_Hardening_Reduce_Attack_Surface
# 11:05:20 11:06:39 CKS_Simulator

# 使用视频章节列表数据分割视频，使用 ffmpeg 工具
# ffmpeg -i input.mp4 -ss 00:00:00 -to 00:02:50 -c copy output.mp4
import os
from click import *
from json import load, loads


@group()
def video() -> None:
    pass


@command(help="Download video")
@argument("input", required=True)
@option("--chapter", help="chapter file", required=False, default=False)
# add boolean option for --skip-download
@option("--skip-download", help="skip download", is_flag=True, default=False)
@option("--src", help="Predownload video src")
def dl(input: str, chapter: bool, skip_download: bool, src: str) -> None:
    # use yt-dlp to download video meta info to a specific json file
    chapter_file = "chapter.info.json"
    args = ["yt-dlp", "--write-info-json", "-o", f"chapter.%(ext)s", input]
    if skip_download:
        args.append("--skip-download")
    code = os.system(" ".join(args))
    if code != 0:
        print("Error: download video chapter")
        return
    chapters = []
    with open(chapter_file, "r", encoding="utf-8") as r:
        data = load(r)
        # chapter info
        chapters = data["chapters"]
    print(chapters[0])
    if not chapters:
        print("Error: no chapters found")
        return
    if skip_download and src:
        for i, chapter in enumerate(chapters):
            start, end, title = (
                int(chapter["start_time"]),
                int(chapter["end_time"]),
                chapter["title"],
            )
            # format seconds to '00:00:00' style
            start = f"{start // 3600:02d}:{start % 3600 // 60:02d}:{start % 60:02d}"
            end = f"{end // 3600:02d}:{end % 3600 // 60:02d}:{end % 60:02d}"
            # ffmpeg split video by start, end
            src_base = os.path.basename(src)
            args = [
                "ffmpeg",
                "-i",
                src,
                "-ss",
                start,
                "-to",
                end,
                "-c",
                "copy",
                f"Part{i+1}_{title.replace(" ", "-")}.webm",
            ]
            code = os.system(" ".join(args))
            if code != 0:
                print("Error: split video")


video.add_command(dl)
