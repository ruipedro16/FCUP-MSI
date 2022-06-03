#!/usr/bin/env sh

if [ "$1" = "-s" ]; then
  pdflatex report.tex >/dev/null 2>&1
  makeindex report.nlo -s nomencl.ist -o report.nls 2>/dev/null
  bibtex report.aux >/dev/null
  pdflatex report.tex >/dev/null 2>&1
  pdflatex report.tex >/dev/null 2>&1
  rm -f report.aux report.bbl report.blg report.ilg report.lof report.log report.nlo report.nls report.out report.toc
else
  pdflatex report.tex
  makeindex report.nlo -s nomencl.ist -o report.nls
  bibtex report.aux
  pdflatex report.tex
  pdflatex report.tex
fi
