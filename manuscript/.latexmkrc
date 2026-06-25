# latexmk configuration for the thesis manuscript

$pdf_mode = 1;
$interaction = 'nonstopmode';
$synctex = 1;

# Keep build products inside the manuscript directory so repository-level
# generated artifacts remain separate from manuscript build artifacts.
$out_dir = 'build';
$aux_dir = 'build';

# Treat warnings as visible in logs but do not change the document source.
$pdflatex = 'pdflatex %O -interaction=nonstopmode -file-line-error %S';
