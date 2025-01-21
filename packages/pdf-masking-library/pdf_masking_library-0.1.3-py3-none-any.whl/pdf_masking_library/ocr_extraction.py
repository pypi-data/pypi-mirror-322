import re
from lxml import html
import logging

from .logger_config import setup_logger
# from .custom_patterns import get_custom_pattern

logger = setup_logger(log_file="masking_app.log", log_level=logging.DEBUG)

def extract_coordinates_from_hocr(hocr_content, page_num, custom_pattern = None):
    
    p1 = re.compile(r'bbox((\s+\d+){4})')
    p2 = re.compile(r'baseline((\s+[\d\.\-]+){2})')
    fourdigitnum = re.compile(r'(?:\S*\s*)?\b(\d{4}).*')   # Matches 4-digit numbers, often for Aadhar
    twelvedigitnum = re.compile(r'.*(\d{12}).*') 
    pan = re.compile(r'[A-Z]{5}(?=.*\d)[A-Z0-9]{4}[A-Z|0-9]')
    thumb = re.compile(r'([Tt]humb)')
    # pattern = re.compile(custom_pattern)


    aadhaar_coords = []  # Aadhaar coordinates
    pan_coords = []      # PAN coordinates
    thumb_coords = []    # Thumb keyword coordinates
    
    # custom_patterns = get_custom_pattern()
    custom_coords = []

    try:
    # Sanitize HOCR content to remove XML declarations
        sanitized_hocr = re.sub(r'<\?xml.*?\?>', '', hocr_content, count=1).strip()
        hocr = html.fromstring(sanitized_hocr)
        
        lines = hocr.xpath('//*[@class="ocr_line"]')

        for i in range(len(lines)):
            line = lines[i]
            linebox = p1.search(line.attrib['title']).group(1).split()
            try:
                baseline = p2.search(line.attrib['title']).group(1).split()
            except AttributeError:
                baseline = [0, 0]
            
            linebox = [float(i) for i in linebox]
            baseline = [float(i) for i in baseline]
            
            words = line.xpath('.//*[@class="ocrx_word"]')
            
            for j in range(len(words)):
                word = words[j]
                rawtext = word.text_content().strip()
                # if  not re.search(r'\d', rawtext): continue  # Skip empty words
                
                # Get the bounding box of the word
                box = p1.search(word.attrib['title']).group(1).split()
                box = [float(i) for i in box]
                
                x0, y0, x1, y1 = box[0], box[1], box[2], box[3]  
                
                if len(custom_pattern) == 0:
                    
                    # Handle four-digit number patterns with adjacent words
                    if fourdigitnum.search(rawtext):
                        if len(words) > j + 2:
                            rwtxt1 = words[j+1].text_content().strip()
                            rwtxt2 = words[j+2].text_content().strip()
                            if fourdigitnum.search(rwtxt1) and fourdigitnum.search(rwtxt2):
                                # Extract bounding boxes for the next words
                                box1 = [float(i) for i in p1.search(words[j+1].attrib['title']).group(1).split()]
                                box2 = [float(i) for i in p1.search(words[j+2].attrib['title']).group(1).split()]

                                # Calculate the overall bounding box
                                x1_combined = max(box[2], box1[2], box2[2])
                                x0_combined = min(box[0], box1[0], box2[0])
                                y1_combined = max(box[3], box1[3], box2[3])
                                y0_combined = min(y0, y0, y0) 

                                aadhaar_coords.append(
                                    ((x0_combined, y0_combined, x1_combined, y1_combined), page_num)
                                )

                        elif len(words) > j + 1 and len(lines) > i + 1 and len(lines[i + 1].xpath('.//*[@class="ocrx_word"]')) >= 1:
                            wordnl = (lines[i + 1].xpath('.//*[@class="ocrx_word"]'))[0]
                            rwtxt1 = words[j + 1].text_content().strip()
                            rwtxt2 = wordnl.text_content().strip()
                            
                            if fourdigitnum.search(rwtxt1) and fourdigitnum.search(rwtxt2):
                                # nxtlnbox = [float(i) for i in p1.search(lines[i + 1].attrib['title']).group(1).split()]
                                box1 = [float(i) for i in p1.search(words[j + 1].attrib['title']).group(1).split()]
                                box2 = [float(i) for i in p1.search(wordnl.attrib['title']).group(1).split()]
                                
                                # b = polyval(baseline, (box2[0] + box2[2]) / 2 - nxtlnbox[0]) + nxtlnbox[3]

                                x0_combined = min(box[0], box1[0])  
                                y0_combined = min(box[1], box1[1])  
                                x1_combined = max(box[2], box1[2])  
                                y1_combined = max(box[3], box1[3]) 

                                aadhaar_coords.append(
                                    ((box2[0], box2[1], box2[2], box2[3]), page_num) 
                                )
                                aadhaar_coords.append(
                                    ((x0_combined, y0_combined, x1_combined, y1_combined), page_num)  
                                )

                            # Case 1: 4 digits on the current line and first 4 digits of 8-digit Aadhaar number on next line
                            # if fourdigitnum.search(rwtxt1) and fourdigitnum.search(rwtxt2):
                            #     nxtlnbox = [float(i) for i in p1.search(lines[i + 1].attrib['title']).group(1).split()]
                            #     box1 = [float(i) for i in p1.search(words[j + 1].attrib['title']).group(1).split()]
                            #     box2 = [float(i) for i in p1.search(wordnl.attrib['title']).group(1).split()]
                                
                            #     b = polyval(baseline, (box2[0] + box2[2]) / 2 - nxtlnbox[0]) + nxtlnbox[3]

                            #     # Mask the first 4 digits in the current line
                            #     aadhaar_coords.append(
                            #         ((box[0], box[1], box[2], box[3]),page_num)  # Mask first part (4 digits)
                            #     )

                            #     # Mask the first 4 digits of the 8 digits on the next line
                            #     aadhaar_coords.append(
                            #         ((box1[0], box1[1], box1[2], box1[3]), page_num)  # Mask second part (first 4 digits of 8 digits)
                            #     )

                            #     # Mask the second 4 digits of the 8 digits on the next line
                            #     aadhaar_coords.append(
                            #         ((box2[0], box2[1], box2[2], box2[3]), page_num)  # Mask third part (second 4 digits of 8 digits)
                            #     )
                            
                            # Case B: Current line contains 4 digits, next line contains 8 digits
                        elif len(lines) > i + 1 and len(lines[i + 1].xpath('.//*[@class="ocrx_word"]')) >= 2:
                            words_next_line = lines[i + 1].xpath('.//*[@class="ocrx_word"]')
                            rwtxt1_next_line = words_next_line[0].text_content().strip()
                            rwtxt2_next_line = words_next_line[1].text_content().strip()

                            if fourdigitnum.search(rwtxt1_next_line) and fourdigitnum.search(rwtxt2_next_line):
                                box1_next_line = [float(k) for k in p1.search(words_next_line[0].attrib['title']).group(1).split()]
                                box2_next_line = [float(k) for k in p1.search(words_next_line[1].attrib['title']).group(1).split()]
                                
                                x0_combined = min(box1_next_line[0], box2_next_line[0])
                                y0_combined = min(box1_next_line[1], box2_next_line[1])  
                                x1_combined = max(box1_next_line[2], box2_next_line[2])  
                                y1_combined = max(box1_next_line[3], box2_next_line[3]) 

                                aadhaar_coords.append(((box[0], box[1], box[2], box[3]), page_num))  
                                # aadhaar_coords.append(((box1_next_line[0], box1_next_line[1], box1_next_line[2], box1_next_line[3]), page_num))  # Next 4 digits
                                # aadhaar_coords.append(((box2_next_line[0], box2_next_line[1], box2_next_line[2], box2_next_line[3]), page_num)) 
                                aadhaar_coords.append(
                                    ((x0_combined, y0_combined, x1_combined, y1_combined), page_num)  
                                )

                    if twelvedigitnum.search(rawtext):
                        aadhaar_coords.append(
                            ((x0, y0, x1, y1), page_num)
                        )
                    
                    if pan.search(rawtext):
                        pan_coords.append(
                            ((x0, y0, x1, y1), page_num)
                        )
                    
                    if thumb.search(rawtext):
                        thumb_coords.append(
                            ((x0, y0, x1, y1), page_num)
                        )
                else:
                    for pattern in custom_pattern:
                        if isinstance(pattern, re.Pattern) and pattern.search(rawtext):
                            custom_coords.append(
                                ((x0, y0, x1, y1), page_num)
                            )
                    # if isinstance(custom_pattern, re.Pattern) and custom_pattern.search(rawtext):
                    #     custom_coords.append(((x0,y0,x1,y1),page_num))
                    

    except Exception as e:
        logger.error(f"Error parsing HOCR data: {e}")

    return aadhaar_coords, pan_coords, thumb_coords, custom_coords