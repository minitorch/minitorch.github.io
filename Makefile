INPUTS = $(wildcard *.py) $(wildcard */*.py)

OUTPUTS = $(patsubst %.py,%.ipynb,$(INPUTS))
TMP = $(patsubst %.py,%.out,$(INPUTS))
CHECKS = $(patsubst %.py,%.check.html,$(INPUTS))

SLIDES_IN = $(wildcard slides/*/*.py)
SLIDES =  $(patsubst %.py,%.slides.html,$(SLIDES_IN))
SLIDES_PDF = $(patsubst %.py,%.slides.pdf,$(SLIDES_IN))

MOVIE_IN = $(wildcard slides.video/*/*.py)
MOVIE =  $(patsubst %.py,%.slides.html,$(MOVIE_IN))
MOVIE_PDF =  $(patsubst %.py,%.slides.pdf,$(MOVIE_IN))


all: $(OUTPUTS)
tmp: $(TMP)
slides: $(SLIDES)
slides_pdf: $(SLIDES_PDF)
movie: $(MOVIE)
movie_pdf: $(MOVIE_PDF)
checks: $(CHECKS)


%.ipynb : %.py
	python $<
	jupytext --execute --set-kernel minitorch --run-path . --to notebook $< 

%.slides.html : %.ipynb
	jupyter nbconvert  $< --to slides --ExecutePreprocessor.kernel_name minitorch --SlidesExporter.reveal_transition="none" --template slides/talk/ --SlidesExporter.reveal_url_prefix="https://unpkg.com/reveal.js@4.3.1"

%.slides.pdf : %.slides.html
	 chromium --headless=new --run-all-compositor-stages-before-draw --virtual-time-budget=100000000 --print-to-pdf "http://localhost:8910/$<?print-pdf" ; mv output.pdf $@

%.html : %.ipynb
	jupyter nbconvert  $< --to html


%.out : %.py
	python $< > $@

