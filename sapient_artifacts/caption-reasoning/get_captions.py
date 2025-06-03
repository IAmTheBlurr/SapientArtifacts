""" Main file that will be used to run the program. """
from modules import TargetVideo, WebVTT

if __name__ == '__main__':
    erics_geometric_unity_presentation = 'Z7rd04KzLcg'
    what_nobody_tells_you_about_documentation = 't4vKPhjcMZg'
    why_4d_geometry_makes_me_sad = 'piJkuavhV50'
    the_geometric_unity_iceberg = 'AThFAxF7Mgw'
    triggernometry_meets_guilty_feminist = 'bgO2G4_F4EQ'

    current_target = triggernometry_meets_guilty_feminist
    file_name = 'triggernometry_meets_guilty_feminist'

    target = TargetVideo(current_target, file_name)
    target.download_captions()

    captions = WebVTT(f'{file_name}.en.vtt')
    caption_text = captions.get_only_captions_text(strip_headers=True)

    # Save the captions to a file marked with 'cleaned'
    with open(f'{file_name}_cleaned_captions.txt', 'w', encoding='utf-8') as file:
        caption_text = caption_text.replace('&nbsp;', '')
        file.write(caption_text)
