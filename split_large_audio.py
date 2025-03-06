import os
import logging
from pydub import AudioSegment
import config

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='audio_processing.log', filemode='a')

def get_file_size_mb(file_path):
    """Получить размер файла в мегабайтах."""
    return os.path.getsize(file_path) / (1024 * 1024)

def segment_audio(input_file, output_dir, max_size):
    """Разделение аудиофайла на равные сегменты по числу count_chunk."""
    logging.info(f"Загрузка аудиофайла: {input_file}")
    print("Идет выполнение процесса...")
    audio = AudioSegment.from_file(input_file)
    file_size = get_file_size_mb(input_file)

    if file_size <= max_size:
        print(f"Файл меньше {max_size} МБ. Обработка не требуется.")
        logging.info(f"Файл {input_file} меньше {max_size} МБ. Обработка пропущена.")
        return

    count_chunk = int(file_size / max_size) + (1 if file_size % max_size > 0 else 0)
    chunk_duration = len(audio) // count_chunk

    print(f"Файл больше {max_size} МБ. Разделяем на {count_chunk} сегментов...")

    os.makedirs(output_dir, exist_ok=True)

    segment_start = 0
    for i in range(count_chunk):
        segment_end = segment_start + chunk_duration
        if segment_end > len(audio):
            segment_end = len(audio)

        chunk = audio[segment_start:segment_end]
        output_path = os.path.join(output_dir, f"{input_file}_chunk_{i + 1}.mp3")
        chunk.export(output_path, format="mp3")
        logging.info(f"Сохранен сегмент: {output_path}")
        print(f"Сохранен сегмент: {output_path}")

        segment_start = segment_end

    print("Процесс завершен. Все сегменты сохранены в папке:", output_dir)
    logging.info("Обработка завершена.")

def main():
    try:
        print("Текущая рабочая директория:", os.getcwd())
        print("Файлы в текущей директории:", os.listdir(os.getcwd()))  # Отладочная информация
        file_name = input("Введите название файла (например, file.mp3): ").strip()
        input_file = os.path.join(os.getcwd(), 'input_file',file_name)

        if not os.path.exists(input_file):
            print(f"Файл не найден: {input_file}")
            logging.error(f"Файл не найден: {input_file}")
            return

        segment_audio(
            input_file=input_file,
            output_dir=config.OUTPUT_DIR,
            max_size=config.MAX_SIZE,
        )
    except FileNotFoundError as e:
        logging.error(f"Файл не найден: {e}")
        print("Файл не найден. Проверьте путь и повторите попытку.")
    except Exception as e:
        logging.exception(f"Произошла ошибка: {e}")
        print("Произошла ошибка. Подробности записаны в лог.")

if __name__ == "__main__":
    main()