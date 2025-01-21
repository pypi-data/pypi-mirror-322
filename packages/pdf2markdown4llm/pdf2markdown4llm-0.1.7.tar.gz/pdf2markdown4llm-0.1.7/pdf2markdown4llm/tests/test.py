from pdf2markdown4llm import PDF2Markdown4LLM


converter = PDF2Markdown4LLM(remove_headers=False, table_header="### Table")

md_content = converter.convert(r"pdf2markdown4llm\tests\SystemConfigurationandTroubleshootingManual.pdf")
with open(r"pdf2markdown4llm\tests\SystemConfigurationandTroubleshootingManual.md", "r", encoding="utf-8") as md_file:
    expected_md_content = md_file.read()
    
assert md_content == expected_md_content, "Markdown content does not match the expected content."

def progress_callback(progress): 
    print(f"Phase: {progress.phase.value}, Page {progress.current_page}/{progress.total_pages}, Progress: {progress.percentage:.1f}%, Message: {progress.message}")


converter = PDF2Markdown4LLM(remove_headers=False, table_header="### Table", progress_callback=progress_callback)

md_content = converter.convert(r"pdf2markdown4llm\tests\SystemConfigurationandTroubleshootingManual.pdf")
with open(r"pdf2markdown4llm\tests\SystemConfigurationandTroubleshootingManual.md", "r", encoding="utf-8") as md_file:
    expected_md_content = md_file.read()
    
assert md_content == expected_md_content, "Markdown content does not match the expected content."


converter = PDF2Markdown4LLM(remove_headers=False, table_header="### Table", skip_empty_tables=True)

md_content = converter.convert(r"pdf2markdown4llm\tests\ligatures_test1.pdf")
with open(r"pdf2markdown4llm\tests\ligatures_test1.md", "r", encoding="utf-8") as md_file:
    expected_md_content = md_file.read()
    
assert md_content == expected_md_content, "Markdown content does not match the expected content."


md_content = converter.convert(r"pdf2markdown4llm\tests\ligatures_test2.pdf")
with open(r"pdf2markdown4llm\tests\ligatures_test2.md", "r", encoding="utf-8") as md_file:
    expected_md_content = md_file.read()
    
assert md_content == expected_md_content, "Markdown content does not match the expected content."

