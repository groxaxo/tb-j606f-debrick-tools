
import os
import xml.etree.ElementTree as ET

def build_super_image(xml_path, output_path):
    print(f"Parsing {xml_path}...")
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
    except Exception as e:
        print(f"Error parsing XML: {e}")
        return

    # Find definition of super_1 to establish base offset
    base_sector = None
    chunks = []
    
    sector_size = 4096 # Default from XML preview

    for prog in root.findall('program'):
        label = prog.get('label')
        filename = prog.get('filename')
        
        if label == 'super' and filename:
            start_sector = int(prog.get('start_sector'))
            s_size = int(prog.get('SECTOR_SIZE_IN_BYTES', 4096))
            sector_size = s_size # Assume constant
            
            # Assume the lowest start_sector is the start of the partition
            if base_sector is None or start_sector < base_sector:
                base_sector = start_sector
            
            chunks.append({
                'filename': filename,
                'start_sector': start_sector
            })

    if base_sector is None:
        print("No super partition chunks found in XML.")
        return

    print(f"Base sector determined as: {base_sector}")
    print(f"Sector size: {sector_size}")

    # precise calculation of file size to pre-allocate?
    # Or just seek and write.
    
    with open(output_path, 'wb') as outfile:
        for chunk in chunks:
            rel_sector = chunk['start_sector'] - base_sector
            byte_offset = rel_sector * sector_size
            
            src_file = os.path.join("firmware_extracted", chunk['filename'])
            
            if not os.path.exists(src_file):
                print(f"Warning: {src_file} not found, skipping.")
                continue
                
            print(f"Writing {chunk['filename']} at offset {byte_offset} bytes (Sector +{rel_sector})...")
            
            outfile.seek(byte_offset)
            
            with open(src_file, 'rb') as infile:
                while True:
                    data = infile.read(1024 * 1024 * 10) # 10MB chunks
                    if not data:
                        break
                    outfile.write(data)
                    
    print(f"Successfully built {output_path}")

if __name__ == "__main__":
    build_super_image("firmware_extracted/rawprogram_unsparse0.xml", "super_fixed.img")
