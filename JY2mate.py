import yt_dlp
import os
from google.colab import files  # Colab에서 파일 다운로드
import hashlib
# import re

# def sanitize_filename(filename):
#     """
#     파일명에서 허용되지 않는 문자를 제거합니다.
#     """
#     return re.sub(r'[\\/*?:"<>|]', "", filename)

def download_all_files(folder_path):
  """
  폴더 내의 모든 파일을 다운로드하는 함수.
  - folder_path: 다운로드할 폴더의 경로
  """
  # 폴더가 존재하는지 확인
  if not os.path.exists(folder_path):
      print(f"폴더가 존재하지 않습니다: {folder_path}")
      return

  # 폴더 내의 모든 파일 다운로드
  for filename in os.listdir(folder_path):
      file_path = os.path.join(folder_path, filename)
      if os.path.isfile(file_path):
          print(f"다운로드 중: {file_path}")
          files.download(file_path)
      else:
          print(f"파일이 아닙니다: {file_path}")

def download_audio(url, download_path="/content/downloads", is_playlist=False):
    """
    유튜브 오디오(MP3)를 다운로드하는 함수.
    - url: 유튜브 URL
    - download_path: 저장 경로
    - is_playlist: 재생목록 여부 (True/False)
    """
    # 다운로드 경로 생성
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    # yt_dlp 옵션 설정
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{download_path}/%(title)s.%(ext)s',
        'quiet': False,
        'ignoreerrors': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
          info_dict = ydl.extract_info(url, download=False)
          video_title = info_dict.get('title', None)#sanitize_filename(info_dict.get('title', None))
          file_extentions = "mp3"
          #file_extentions=info_dict.get('ext',None)
          ldownload_path = os.path.join(download_path, f"{video_title}.{file_extentions}")
          if is_playlist:
                print("재생목록 오디오 다운로드 중...")
                ydl.download([url])

                # ZIP 압축
                zip_file = f"{download_path}.zip"
                os.system(f"zip -r {zip_file} {download_path}")
                print(f"재생목록이 압축되었습니다: {zip_file}")

                # Colab에서 다운로드
                files.download(zip_file)
          else:
                print("단일 오디오 다운로드 중...")
                ydl.download([url])
                print(f"단일 오디오 다운로드 완료: {ldownload_path}")
                folder_path = '/content/downloads'
                download_all_files(folder_path)
                # files.download(ldownload_path)

    except Exception as e:
        print(f"오디오 다운로드 중 오류 발생: {e}")


def download_video(url, download_path="/content/downloads", is_playlist=False):
    """
    유튜브 영상을 다운로드하는 함수.
    - url: 유튜브 URL
    - download_path: 저장 경로
    - is_playlist: 재생목록 여부 (True/False)
    """
    # 다운로드 경로 생성
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    # yt_dlp 옵션 설정
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': f'{download_path}/%(title)s.%(ext)s',
        'quiet': False,
        'ignoreerrors': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
          info_dict = ydl.extract_info(url, download=False)
          video_title = info_dict.get('title', None)#sanitize_filename(info_dict.get('title', None))
          file_extentions=info_dict.get('ext',None)
          ldownload_path = os.path.join(download_path, f"{video_title}.{file_extentions}")
          if is_playlist:
                print("재생목록 영상 다운로드 중...")
                ydl.download([url])

                # ZIP 압축
                zip_file = f"{download_path}.zip"
                os.system(f"zip -r {zip_file} {download_path}")
                print(f"재생목록이 압축되었습니다: {zip_file}")

                # Colab에서 다운로드
                files.download(zip_file)
          else:
                print("단일 영상 다운로드 중...")
                ydl.download([url])
                print(f"단일 영상 다운로드 완료: {ldownload_path}")
                folder_path = '/content/downloads'
                download_all_files(folder_path)
                # files.download(ldownload_path)

    except Exception as e:
        print(f"영상 다운로드 중 오류 발생: {e}")


def main():
    """
    유튜브 다운로드 프로그램의 메인 함수.
    """
    print("JY2mate (Google Colab 환경)")
    print("1. 오디오(MP3) 다운로드")
    print("2. 영상(MP4) 다운로드")
    print("3. 다운로드 폴더 초기화")
    mode_choice = input("다운로드할 모드를 선택하세요 (1: 오디오, 2: 영상, 3: 다운로드 폴더 초기화): ").strip()

    if mode_choice not in ["1", "2", "3"]:
        print("잘못된 선택입니다. 프로그램을 종료합니다.")
        return

    if mode_choice == "3":
      download_path = "/content/downloads"
      if os.path.exists(download_path):
        for filename in os.listdir(download_path):
          os.remove(os.path.join(download_path,filename))
      print("다운로드 폴더가 초기화되었습니다.")
      return

    is_audio = mode_choice == "1"

    print("1. 단일 콘텐츠 다운로드")
    print("2. 재생목록 다운로드")
    content_choice = input("작업 모드를 선택하세요 (1: 단일, 2: 재생목록): ").strip()

    if content_choice not in ["1", "2"]:
        print("잘못된 선택입니다. 프로그램을 종료합니다.")
        return

    is_playlist = content_choice == "2"
    url = input("유튜브 URL을 입력하세요: ").strip()
    download_path = "/content/downloads"  # 기본 다운로드 경로

    # 다운로드 실행
    if is_audio:
        download_audio(url, download_path, is_playlist)
    else:
        download_video(url, download_path, is_playlist)


if __name__ == "__main__":
    # Sample data
    data = input("Enter the licence code")

    # Creating a hash object using the SHA-256 algorithm
    hash_object = hashlib.sha256(data.encode())

    # Getting the hexadecimal representation of the hash
    hex_dig = hash_object.hexdigest()

    # print(f"SHA-256 hash of '{data}' is: {hex_dig}")
    if hex_dig == "7b65ee222af36b78b07cdfa4aebb92b5748803ba9b08befd22ae59eda2af5ea4":
      main()
    else:
      print("잘못된 인증코드입니다. 프로그램을 종료합니다.")
      
