# Compile latex files

for fig in car example house sc tb tc tsb
do
    cd ${fig} && pdflatex slide && rm slide.aux slide.nav slide.log slide.out slide.snm slide.toc && cd .. && cp ${fig}/slide.pdf ${fig}.pdf
done
