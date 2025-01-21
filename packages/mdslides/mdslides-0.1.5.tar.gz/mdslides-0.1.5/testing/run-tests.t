  $ cp -r ${TESTDIR}/Simple ./
  $ ls ./Simple
  simple.md
  $ mdslides ./Simple/simple.md
  Generating slides: Simple/simple.md -> Simple/simple/index.html
  $ ls ./Simple
  simple
  simple.md
  $ ls ./Simple/simple
  index.html
  slidy


  $ cp -r ${TESTDIR}/Processing ./
  $ cd ./Processing
  $ ls
  postprocess
  preprocess
  slides.md
  $ mdslides ./slides.md
  Pre-processing: slides.md -> slides-preprocessed.md
  Generating slides: slides-preprocessed.md -> slides/index.html
  Post-processing: slides/index.html
  $ ls 
  postprocess
  preprocess
  slides
  slides-preprocessed.md
  slides.md
  $ ls ./slides
  index.html
  slidy
  $ cd ..


  $ cp -r ${TESTDIR}/Iframe ./
  $ cd ./Iframe
  $ ls
  hello.html
  iframe.md
  $ mdslides ./iframe.md
  Generating slides: iframe.md -> iframe/index.html
  copying hello.html to iframe
  $ ls 
  hello.html
  iframe
  iframe.md
  $ ls ./iframe
  hello.html
  index.html
  slidy
  $ cd ..
