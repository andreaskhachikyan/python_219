import time
import threading
import multiprocessing
from collections import defaultdict

def count_words(filename):
    word_freq = defaultdict(int)
    with open(filename, 'r') as file:
        for line in file:
            for word in line.strip().split():
                word_freq[word] += 1
    return word_freq

def count_words_thread(chunk, word_freq, lock):
    local_freq = defaultdict(int)
    for line in chunk:
        for word in line.strip().split():
            local_freq[word] += 1
    with lock:
        for word, count in local_freq.items():
            word_freq[word] += count

def multithreaded_word_count(filename, num_threads=4):
    word_freq = defaultdict(int)
    lock = threading.Lock()
    threads = []
    with open(filename, 'r') as file:
        lines = file.readlines()
    chunk_size = len(lines) // num_threads
    for i in range(num_threads):
        start = i * chunk_size
        end = None if i == num_threads - 1 else (i + 1) * chunk_size
        chunk = lines[start:end]
        t = threading.Thread(target=count_words_thread, args=(chunk, word_freq, lock))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    return word_freq

def count_words_process(chunk):
    word_freq = defaultdict(int)
    for line in chunk:
        for word in line.strip().split():
            word_freq[word] += 1
    return word_freq

def multiprocessing_word_count(filename, num_processes=4):
    with open(filename, 'r') as file:
        lines = file.readlines()
    chunk_size = len(lines) // num_processes
    chunks = [lines[i * chunk_size: None if i == num_processes - 1 else (i + 1) * chunk_size] for i in range(num_processes)]
    with multiprocessing.Pool(num_processes) as pool:
        results = pool.map(count_words_process, chunks)
    word_freq = defaultdict(int)
    for local_freq in results:
        for word, count in local_freq.items():
            word_freq[word] += count
    return word_freq

def main():
    filename = 'large_text_file.txt'
    start_time = time.time()
    seq = count_words(filename)
    print(f"Sequential: {time.time() - start_time:.4f}s")
    start_time = time.time()
    thread = multithreaded_word_count(filename)
    print(f"Multithreading: {time.time() - start_time:.4f}s")
    start_time = time.time()
    process = multiprocessing_word_count(filename)
    print(f"Multiprocessing: {time.time() - start_time:.4f}s")

if __name__ == '__main__':
    main()