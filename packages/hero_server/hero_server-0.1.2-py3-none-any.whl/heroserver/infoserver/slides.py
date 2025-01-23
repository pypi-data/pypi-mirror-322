from typing import List, Optional


class Slide:
    def __init__(
        self,
        name: str,
        title: Optional[str] = None,
        notes: Optional[str] = None,
    ):
        self.name: str = name
        self.title: Optional[str] = title
        self.notes: Optional[str] = notes


class Slides:
    def __init__(self):
        self.slides: List[Slide] = []
        self.path: str = ''

    def add_slide(self, slide: Slide):
        self.slides.append(slide)

    def get_slide_by_name(self, name: str) -> Optional[Slide]:
        for slide in self.slides:
            if slide.name == name:
                return slide
        return None

    def parse(self, input_text: str):
        lines = input_text.strip().split('\n')
        for line in lines:
            line = line.strip()
            if line.endswith('.png'):
                slide_name = line
                self.add_slide(Slide(slide_name))
            else:
                pass


if __name__ == '__main__':
    # Input text
    input_text = """
threefold_intro_depin.png
experience.png
worldrecords.png

title_problem.png
threelayers.png
cloud_limitations.png
hardware_powerful.png
layers.png
why_this.png

title_solution.png
trillionusd.png
inventions.png
zos1.png
zos_network.png
arch_layers.png
usecases.png
pricing.png
compare.png

"""

    # Create Slides instance and parse the input
    slides = Slides()
    slides.parse(input_text)

    # Example usage
    print(f'Total number of slides: {len(slides.slides)}')
    print(f'Name of the first slide: {slides.slides[0].name}')
    print(f'Name of the last slide: {slides.slides[-1].name}')

    # Print all slides with their titles (if available)
    for slide in slides.slides:
        if slide.title:
            print(f'Slide: {slide.name}, Title: {slide.title}')
        else:
            print(f'Slide: {slide.name}')

    # Example of getting a slide by name
    team_slide = slides.get_slide_by_name('worldrecords.png')
    if team_slide:
        print(f'Found slide: {team_slide.name}')
    else:
        print('Slide not found')
