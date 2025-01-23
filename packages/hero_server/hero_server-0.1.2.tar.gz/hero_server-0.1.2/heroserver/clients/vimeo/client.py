import os
from typing import List, Optional

import requests
import vimeo
from model_video import VideoInfo, video_model_load, videos_model_load


class VimeoClient:
    def __init__(self):
        # Retrieve necessary credentials from environment variables
        self.client_id = os.getenv("VIMEO_CLIENT_ID")
        self.client_secret = os.getenv("VIMEO_SECRET")
        self.access_token = os.getenv("VIMEO_ACCESSTOKEN_ID")
        self.user_id = os.getenv("VIMEO_USER_ID")

        # Check if all environment variables are present
        if not all([self.client_id, self.client_secret, self.access_token, self.user_id]):
            raise EnvironmentError(
                "Please set the VIMEO_CLIENT_ID, VIMEO_SECRET,VIMEO_USER_ID and VIMEO_ACCESSTOKEN_ID environment variables."
            )

        # Initialize the Vimeo client
        self.client = vimeo.VimeoClient(token=self.access_token, key=self.client_id, secret=self.client_secret)

    def upload(self, file: str, video_title: str, description: str) -> str:
        video_uri = self.client.upload(file, data={"name": video_title, "description": description})
        return video_uri

    def download(self, video_id: str, output_file: str = "myvid.mp4"):
        info = self.get_video_info(video_id)

        size, link = 0, ""
        for item in info.download:
            if item["size"] > size:
                size = item["size"]
                link = item["link"]

        if link == "":
            raise Exception("download link not provided for video")

        video_response = requests.get(link, stream=True)
        downloaded_mb = 0
        with open(output_file, "wb") as video_file:
            for chunk in video_response.iter_content(chunk_size=1024):
                if chunk:
                    downloaded_mb += len(chunk) / 1024
                    print(f"{downloaded_mb}MB Downloaded...")
                    video_file.write(chunk)

        print(f"Video downloaded successfully to {output_file}!")

    def get_video_info(self, video_id: str) -> VideoInfo:
        """
        Get information about a video by URI.
        :param uri: URI of the Vimeo video.
        :return: Video information as a dictionary, or None if an error occurs.
        """
        # , fields: List[str]
        response = self.client.get(f"/videos/{video_id}")
        if response.status_code == 200:
            myvideo = video_model_load(response.content)
        else:
            raise Exception(f"Failed to get video details. Status code: {response.status_code}, Error: {response.text}")
        return myvideo

    def get_videos(self, folder: Optional[int] = None, folders: Optional[List[int]] = None) -> List[VideoInfo]:
        """
        Get information about videos from specified folder(s) or all videos if no folder is specified.
        :param folder: ID of a single folder to fetch videos from.
        :param folders: List of folder IDs to fetch videos from.
        :return: List of VideoInfo objects.
        """
        if self.user_id == 0:
            raise Exception("Can't find user ID, it's not set in env variables")

        all_videos = []

        if folder is not None:
            folders = [folder]
        elif folders is None:
            # If no folder or folders specified, get all videos
            response = self.client.get("/me/videos")
            if response.status_code == 200:
                return videos_model_load(response.content)
            else:
                raise Exception(f"Failed to get videos. Status code: {response.status_code}, Error: {response.text}")
        for folder_id in folders:
            response = self.client.get(f"/users/{self.user_id}/projects/{folder_id}/videos")
            if response.status_code == 200:
                videos = videos_model_load(response.content)
                all_videos.extend(videos)
            else:
                print(f"Failed to get videos for folder {folder_id}. Status code: {response.status_code}, Error: {response.text}")

        return all_videos

    # def get_videos(self,folder:int,folders:List[int]) -> List[VideoInfo]:
    #     """
    #     Get information about a video by URI.
    #     :param uri: URI of the Vimeo video.
    #     :return: Video information as a dictionary, or None if an error occurs.
    #     """
    #     if folder>0:
    #         if self.user_id == 0:
    #             return Exception("can't find userid, its not set in env variables")
    #         # print(f"folderid:{folder}")
    #         response = self.client.get(f"/users/{self.user_id}/projects/{folder}/videos")
    #         # api_url = f"https://api.vimeo.com/users/{self.user_id}/projects/13139570/videos"
    #         # print(api_url)
    #         # access_token = "e65daca3b0dbc18c2fadc5cafcf81004"
    #         # headers = {
    #         #     "Authorization": f"Bearer {access_token}"
    #         # }
    #         # Make the GET request to the Vimeo API
    #         #response = requests.get(api_url, headers=headers)
    #     else:
    #         response = self.client.get(f"/me/videos/")

    #     if response.status_code == 200:
    #         myvideos = videos_model_load(response.content)
    #     else:
    #         raise Exception(f"Failed to get video details. Status code: {response.status_code}, Error: {response.text}")
    #     return myvideos


def new() -> VimeoClient:
    return VimeoClient()


# Example usage:
if __name__ == "__main__":
    cl = new()
    v = cl.get_videos(folders=[10700101, 13139570, 12926235, 10752310, 10702046])
    for item in v:
        video_id = item.uri.split("/")[-1]
        print(f" - {item.name} : {video_id} ")
        # from IPython import embed; embed()
        # s
    # vi=cl.get_video_info("475353425")
    # print(json_to_yaml(vi))
    # cl.download("475353425", "/tmp/475353425.mp4")
