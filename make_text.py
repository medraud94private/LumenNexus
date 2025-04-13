import os
import csv

def main():
    # 현재 스크립트가 있는 절대 경로를 구합니다.
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 자신의 스크립트 파일 경로 (제외 대상)
    script_path = os.path.abspath(__file__)
    
    # 결과를 저장할 리스트 (각 항목은 [제목, 본문] 형태)
    results = []

    # os.walk를 사용하여 현재 디렉토리 및 하위 디렉토리를 순회
    for root, dirs, files in os.walk(current_dir):
        for file in files:
            # 확장자가 .py 인 파일 선택
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                # 자신의 스크립트 파일인 경우는 건너뜁니다.
                if os.path.abspath(file_path) == script_path:
                    continue
                # 파일 내용을 읽습니다.
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
                    content = ""
                # 파일 이름을 제목으로, 내용을 본문으로 리스트에 추가합니다.
                results.append([file, content])
                
    # CSV 파일로 결과 저장 (헤더: 제목, 본문)
    output_csv = os.path.join(current_dir, 'python_files.csv')
    try:
        with open(output_csv, 'w', encoding='utf-8', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['제목', '본문'])
            writer.writerows(results)
        print(f"CSV 파일이 생성되었습니다: {output_csv}")
    except Exception as e:
        print(f"CSV 파일 생성 중 오류가 발생했습니다: {e}")

if __name__ == '__main__':
    main()
