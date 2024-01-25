# 상공회의소 경기인력개발원 인텔교육 1기

## Clone code 

```shell
git clone --recurse-submodules https://github.com/kgkorchamhrd/intel-01.git
```

* `--recurse-submodules` option 없이 clone 한 경우, 아래를 통해 submodule update

```shell
git submodule update --init --recursive
```

## Preparation

### Git LFS(Large File System)

* 크기가 큰 바이너리 파일들은 LFS로 관리됩니다.

* git-lfs 설치 전

```shell
# Note bin size is 132 bytes before LFS pull

$ find ./ -iname *.bin|xargs ls -l
-rw-rw-r-- 1 <ID> <GROUP> 132 Nov  6 09:41 ./mosaic-9.bin
-rw-rw-r-- 1 <ID> <GROUP> 132 Nov  6 09:41 ./mosaic-9.bin
-rw-rw-r-- 1 <ID> <GROUP> 132 Nov  6 09:41 ./ssdlite_mobilenet_v2_fp16.bin
-rwxrwxr-x 1 <ID> <GROUP> 132 Nov  6 09:41 ./ssdlite_mobilenet_v2_fp16.bin
```

* git-lfs 설치 후, 다음의 명령어로 전체를 가져 올 수 있습니다.

```shell
$ sudo apt install git-lfs

$ git lfs pull
$ find ./ -iname *.bin|xargs ls -l
-rw-rw-r-- 1 <ID> <GROUP> 3358630 Nov  6 09:41 ./mosaic-9.bin
-rw-rw-r-- 1 <ID> <GROUP> 3358630 Nov  6 09:41 ./mosaic-9.bin
-rw-rw-r-- 1 <ID> <GROUP> 8955146 Nov  6 09:41 ./ssdlite_mobilenet_v2_fp16.bin
-rwxrwxr-x 1 <ID> <GROUP> 8955146 Nov  6 09:41 ./ssdlite_mobilenet_v2_fp16.bin
```

### 환경설정

* [Ubuntu](./doc/environment/ubuntu.md)
* [OpenVINO](./doc/environment/openvino.md)
* [OTX](./doc/environment/otx.md)

## Team projects

### 제출방법

1. 팀구성 및 프로젝트 세부 논의 후, 각 팀은 프로젝트 진행을 위한 Github repository 생성

2. [doc/project/README.md](./doc/project/README.md)을 각 팀이 생성한 repository의 main README.md로 복사 후 팀 프로젝트에 맞게 수정 활용

3. 과제 제출시 `인텔교육 3기 Github repository`에 `New Issue` 생성. 생성된 Issue에 하기 내용 포함되어야 함.

    * Team name : Project Name
    * Project 소개
    * 팀원 및 팀원 역활
    * Project Github repository
    * Project 발표자료 업로드

4. 강사가 생성한 `Milestone`에 생성된 Issue에 추가 

### 평가방법

* [assessment-criteria.pdf](./doc/project/assessment-criteria.pdf) 참고

### 제출현황

### Team: 뭔가 센스있는 팀명
<프로젝트 요약>
* Members
  | Name | Role |
  |----|----|
  | 이찬솔 | Project lead, AI modeling, 프로젝트를 총괄한다. |
  | 정가희 | Project manager, Embedded programming 프로젝트 이슈 진행상황을 관리한다. |
  | 윤용빈 | AI modeling, 원하는 결과가 나오도록 AI model을 선택, data 수집, training을 수행한다. |
  | 노재희 | AI modeling, 원하는 결과가 나오도록 AI model을 선택, data 수집, training을 수행한다. |
* Project Github : https://github.com/chansol1604/project_Ai_ad.git
* 발표자료 : https://github.com/goodsense/project_aewsome/doc/slide.ppt


* ### Team: Team GPT
<프로젝트 요약>
* Members
  | Name | Role |
  |----|----|
  | 강이삭 | Project lead, pretrain 모델 결정, custom train model 학습, data라벨링, 프로젝트를 총괄한다. |
  | 이성찬 | Project manager, custom train model 의 Predict 코드 작성, 하드웨어 제어 코드 작성, 가이드 라인 제시. |
  | 이영호 | jetson - raspberrypy 간 통신, data 수집, 하드웨어 제어 코드 작성, data 라벨링 |
  | 김경민 | rc-car 하드웨어 제작, 트랙 제작, data 수집, data 라벨링, 정보 수집 을 수행한다. |
  | 조현욱 | data 수집, jetson - raspberrypy 간 통신, 하드웨어 제어 코드 작성. |
* Project Github : https://github.com/82lilsak/automatic_driving_rc_car.git
* 발표자료 : https://docs.google.com/presentation/d/1lcZgRt2UtX3FBcI--Va3W0HJIWWH3JD9IqRSMXDPwtM/edit?usp=sharing

* ### Team: Intel Parking lot
<프로젝트 요약>
이제껏 배운 기술을 총동원하여 주차장 시스템을 구현해내는 프로젝트
* Members
  | Name | Role |
  |----|----|
  | 문정환 | Project lead 프로젝트를 총괄한다. |
  | 강태의 | Technical lead : 기술적 난점을 해결한다. |
  | 강대욱 | Architecter : 상위레벨 디자인을 책임진다. |
  | 한상훈 |  AI modeling, 원하는 결과가 나오도록 AI model을 선택, data 수집, training을 수행한다.|
* Project Github : https://github.com/HardCoding0417/Parking-lot-project
* 발표자료 : https://github.com/HardCoding0417/Parking-lot-project/tree/main/doc/presentation.odp
