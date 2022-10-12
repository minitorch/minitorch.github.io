INPUTS = $(wildcard *.py) $(wildcard */*.py)

OUTPUTS = $(patsubst %.py,%.ipynb,$(INPUTS))
TMP = $(patsubst %.py,%.out,$(INPUTS))
CHECKS = $(patsubst %.py,%.check.html,$(INPUTS))

SLIDES_IN = $(wildcard */*/*.py)
SLIDES =  $(patsubst %.py,%.slides.html,$(SLIDES_IN))



all: $(OUTPUTS)
tmp: $(TMP)
slides: $(SLIDES)
checks: $(CHECKS)

%.ipynb : %.py
	jupytext --execute --run-path . --to notebook $<

%.slides.html : %.ipynb
	jupyter nbconvert  $< --to slides --SlidesExporter.reveal_transition="none" --template slides/talk/ --SlidesExporter.reveal_url_prefix="https://unpkg.com/reveal.js@4.3.1"


%.html : %.ipynb
	jupyter nbconvert  $< --to html


%.out : %.py
	python $< > $@

