import os
import time
from openpyxl import Workbook

def get_folders_by_creation_date(base_path, target_date):
    result = []
    for item in os.listdir(base_path):
        item_path = os.path.join(base_path, item)
        if os.path.isdir(item_path):
            creation_time = os.path.getctime(item_path)
            creation_date = time.strftime('%Y-%m-%d', time.localtime(creation_time))
            if creation_date == target_date:
                result.append((item_path, creation_time))
                print(f"Pasta encontrada: {item_path} com data de criação {creation_date}")
    result.sort(key=lambda x: x[1]) 
    return result

def get_last_subfolder(folder_path):
    subfolders = [os.path.join(folder_path, d) for d in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, d))]
    if subfolders:
        last_subfolder = max(subfolders, key=os.path.getctime)
        print(f"Última subpasta em {folder_path}: {last_subfolder}")  
        return last_subfolder
    return None

def get_last_tif_file_name_as_number(folder_path):
    last_file = None
    for root, dirs, files in os.walk(folder_path):
        tif_files = [file for file in files if file.endswith(".tif")]
        if tif_files:
            last_file = max(tif_files, key=lambda f: os.path.getctime(os.path.join(root, f)))
    
    if last_file:
        tif_file_name = os.path.splitext(last_file)[0]
        try:
            tif_file_number = int(tif_file_name.lstrip('0'))  
        except ValueError:
            tif_file_number = tif_file_name 
        print(f"Último arquivo TIF encontrado em {folder_path}: {tif_file_name}.tif -> Número: {tif_file_number}")  
        return tif_file_number

    print(f"Nenhum arquivo TIF encontrado em {folder_path}")  
    return None

def main():
    base_path = input("Digite o local de procura (Formato: ///): ")
    target_date = input("Digite a data da pesquisa (Formato: AAAA-MM-DD): ") # Formato: 'YYYY-MM-DD'
    
    folders = get_folders_by_creation_date(base_path, target_date)
    print(f"Pastas encontradas: {folders}")  
    
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Pastas e Quantidade de Arquivos"
    
    sheet.append(["Processo", "Imagem"])
    
    for folder, creation_time in folders:
        folder_name = os.path.basename(folder)
        print(f"Analisando pasta: {folder_name}")  
        last_subfolder = get_last_subfolder(folder)
        if last_subfolder:
            file_number = get_last_tif_file_name_as_number(last_subfolder)
            if file_number is not None:
                sheet.append([folder_name, file_number])
            else:
                sheet.append([folder_name, "N/a"])
        else:
            sheet.append([folder_name, "Nenhuma subpasta encontrada"])
    
    workbook.save("C:/Users/Gustavo/Desktop/pastas_e_quantidade_de_arquivos.xlsx")
    print("Planilha salva como 'pastas_e_quantidade_de_arquivos.xlsx'")  

if __name__ == "__main__":
    main()

print("Planilha com dados por data gerado!")
time.sleep(7)
