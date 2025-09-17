import re
import sys

def extract_words(text):
    words = []
    # 匹配每行中的英文单词（忽略词性和解释）
    pattern = r'^([a-zA-Z-]+)\s+[a-zA-Z.]*\s*'
    
    for line in text.split('\n'):
        line = line.strip()
        if line:
            match = re.match(pattern, line)
            if match:
                words.append(match.group(1))
    return words

def main(input_file, output_file):
    try:
        # 读取输入文件
        with open(input_file, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # 提取单词
        words = extract_words(content)
        
        # 写入输出文件
        with open(output_file, 'w', encoding='utf-8') as file:
            for word in words:
                file.write(f"{word}\n")
        
        print(f"成功提取 {len(words)} 个单词并保存到 {output_file}")
                
    except FileNotFoundError:
        print(f"错误：文件 '{input_file}' 不存在")
        sys.exit(1)
    except Exception as e:
        print(f"错误：发生未知错误 - {e}")
        sys.exit(1)

if __name__ == "__main__":
    main("wordlib/考研_init.txt", "../wordlib/考研.txt")