
from nutriscan.extractor import extract_saturated_fat_block

sample_text = """
14.9 g°                    14%°
Saturated Fat™          OR           OR
7.6 9°        7%"
"""

result = extract_saturated_fat_block(sample_text)

print("\nSATURATED FAT EXTRACTION\n")
print(result)
