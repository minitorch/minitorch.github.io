INPUTS = $(wildcard *.py) $(wildcard */*.py)

OUTPUTS = $(patsubst %.py,%.ipynb,$(INPUTS))
CHECKS = $(patsubst %.py,%.check.html,$(INPUTS))

SLIDES_IN = $(wildcard */*/*.py)
SLIDES =  $(patsubst %.py,%.slides.html,$(SLIDES_IN)) 



all: $(OUTPUTS)
slides: $(SLIDES)
checks: $(CHECKS)

%.ipynb : %.py
	jupytext --execute --run-path .. --to notebook $<

%.slides.html : %.ipynb
	jupyter nbconvert  $< --to slides --SlidesExporter.reveal_transition="none" --template slides/talk


%.html : %.ipynb
	jupyter nbconvert  $< --to html

