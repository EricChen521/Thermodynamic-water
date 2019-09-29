#!/bin/csh
# set location of gistpp
set dir="/home/users/laurenw/Gist-Post-Processing-master"

# you need the following files
# 1) gist-output.dat
# 2) gist-gO.dx
# 3) ligand.pdb (pdb file of ligand -should be allgned in the binding site)

set dir="/home/users/laurenw/Gist-Post-Processing-master"

# set maximum integration distance
set dist = 6 

# energy of bulk water reference - set to a positive values because it is involved in an addition operation in the code
set refE=9.533

# number of frames in your gist trajectory
set frames=100000
echo $frames > FRAME
set framefactor=`awk '{printf "%f\n",(1/$1)}' FRAME`
rm FRAME
# i defines integration
# for example, when i=5, the volume of interest for us is within 5 Å of any ligand heavy atom. 
set i=5
#set final value based on size of box
while ( $i < $dist )


  mkdir process.data.within.$i 

  $dir/gistpp -i gist-gO.dx -i2 ligand.pdb -op defbp -opt const $i -o ligand_within.$i.dx


#isolate the columns we want to add into their own files
#column 12 is Esw-norm(kcal/mol/water molecule) and has 8 digits past the decimal
#column 14 is Eww-norm-unref(kcal/mol/water molecule) and has 5 digits past the decimal
  $dir/gistpp -i gist-output.dat -i2 gist-gO.dx -op makedx -opt const 12 -o 12.dx
  $dir/gistpp -i ligand_within.$i.dx -i2 12.dx -op mult -o Esw.within.$i.dx

  $dir/gistpp -i gist-output.dat -i2 gist-gO.dx -op makedx -opt const 14 -o 14.dx
  $dir/gistpp -i ligand_within.$i.dx -i2 14.dx -op mult -o Eww.within.$i.dx
#add the columns together into a new file called gist-Etot-norm.dx
  $dir/gistpp -i 12.dx -i2 14.dx -op add -o gist-Etot-norm.dx
  $dir/gistpp -i ligand_within.$i.dx -i2 gist-Etot-norm.dx -op mult -o Etot.norm.within.$i.dx

#now we can subtract bulk water from this
#try with -$refEkcal/mol/water molecule
#output to gist-Eww-norm.dx - Eww (14.dx) relative bulk water
#output to gist-Etot-rel.dx -- Etot relative to bulk water
#when you open in VMD, bulk water will be at value 0
  $dir/gistpp -i 14.dx -op addconst -opt const $refE -o gist-Eww-rel.dx
  $dir/gistpp -i ligand_within.$i.dx -i2 gist-Eww-rel.dx -op mult -o Eww-rel.norm.within.$i.dx
  $dir/gistpp -i gist-Etot-norm.dx -op addconst -opt const $refE -o gist-Etot-rel.dx
  $dir/gistpp -i ligand_within.$i.dx -i2 gist-Etot-rel.dx -op mult -o Etot-rel.norm.within.$i.dx
#Population of water molecules
  $dir/gistpp -i gist-output.dat -i2 gist-gO.dx -op makedx -opt const 4 -o pop.dx
  $dir/gistpp -i ligand_within.$i.dx -i2 pop.dx -op mult -o pop.within.$i.dx
# update value based on size of trajectory $framefactor for 100 ns and 0.00002 for 50 ns 
  $dir/gistpp -i pop.within.$i.dx -op multconst -opt const $framefactor -o percent_pop.within.$i.dx
# Energy terms - units kcal/mol
# Esw
  $dir/gistpp -i percent_pop.within.$i.dx -i2  Esw.within.$i.dx -op mult -o gist-Esw-within.$i.dx
# Eww
  $dir/gistpp -i percent_pop.within.$i.dx -i2  Eww.within.$i.dx -op mult -o gist-Eww-within.$i.dx
# dEww
  $dir/gistpp -i percent_pop.within.$i.dx -i2 Eww-rel.norm.within.$i.dx -op mult -o gist-Eww-rel-within.$i.dx
#dEtot
  $dir/gistpp -i percent_pop.within.$i.dx -i2 Etot-rel.norm.within.$i.dx -op mult -o gist-Etot-rel-within.$i.dx
# integration step for different energy terms
  $dir/gistpp -i gist-Esw-within.$i.dx -op sum | grep sum | awk '{print"Esw",$5}' > tmp.Esw 
  $dir/gistpp -i gist-Eww-within.$i.dx -op sum | grep sum | awk '{print"Eww",$5}' > tmp.Eww
  $dir/gistpp -i gist-Eww-rel-within.$i.dx -op sum | grep sum | awk '{print"dEww",$5}' > tmp.dEww
  $dir/gistpp -i gist-Etot-rel-within.$i.dx -op sum | grep sum | awk '{print"dEtot",$5}' > tmp.dEtot


#get the temperature weighted entropy - kcal/mol/water molecule
  $dir/gistpp -i gist-output.dat -i2 gist-gO.dx -op makedx -opt const 8 -o trans.dx
  $dir/gistpp -i ligand_within.$i.dx -i2 trans.dx -op mult -o trans.within.$i.dx
  $dir/gistpp -i gist-output.dat -i2 gist-gO.dx -op makedx -opt const 10 -o orient.dx
  $dir/gistpp -i ligand_within.$i.dx -i2 orient.dx -op mult -o orient.within.$i.dx
  $dir/gistpp -i trans.dx -i2 orient.dx -op add -o total.entropy.norm.dx
  $dir/gistpp -i ligand_within.$i.dx -i2 total.entropy.norm.dx -op mult -o total.entropy.norm.within.$i.dx
#temperature weighted entropy - kcal/mol 
  $dir/gistpp -i trans.within.$i.dx -i2 percent_pop.within.$i.dx -op mult -o gist.trans-pop.within.$i.dx
  $dir/gistpp -i orient.within.$i.dx -i2 percent_pop.within.$i.dx -op mult -o gist.orient-pop.within.$i.dx
  $dir/gistpp -i total.entropy.norm.within.$i.dx -i2 percent_pop.within.$i.dx -op mult -o gist.total.entropy-within.$i.dx

#integration step for different entropy terms 
  $dir/gistpp -i gist.trans-pop.within.$i.dx -op sum | grep sum | awk '{print"TdStrans",$5}' > TdStrans.tmp
  $dir/gistpp -i gist.orient-pop.within.$i.dx -op sum | grep sum | awk '{print"TdSorient",$5}' > TdSorient.tmp
  $dir/gistpp -i gist.total.entropy-within.$i.dx -op sum | grep sum | awk '{print"TdStotal",$5}' > TdStotal.tmp

#waters in the region of integration
  $dir/gistpp -i percent_pop.within.$i.dx -op sum | grep sum | awk '{print"#waters",$5}' > waters.tmp


  cat tmp.Esw tmp.Eww tmp.dEww tmp.dEtot TdStrans.tmp TdSorient.tmp TdStotal.tmp waters.tmp > GIST.within.$i.summary 

  rm *.tmp tmp.* 
  mv 12.dx 14.dx process.data.within.$i/
  mv gist-E* process.data.within.$i/
  mv *within.$i.dx process.data.within.$i/
  mv trans.dx orient.dx *pop* total.entropy* process.data.within.$i/

#organize time dependent data
  echo $i >> distance.tmp.A
  grep Esw GIST.within.$i.summary | awk '{print$2}' >> Esw.distance.tmp.A
  grep Eww GIST.within.$i.summary | grep -v d | awk '{print$2}' >> Eww.distance.tmp.A 
  grep dEww GIST.within.$i.summary | awk '{print$2}' >> dEww.distance.tmp.A 
  grep dEtot GIST.within.$i.summary | awk '{print$2}' >> dEtot.distance.tmp.A 
  grep TdStrans GIST.within.$i.summary | awk '{print$2}' >> TdStrans.distance.tmp.A 
  grep TdSorient GIST.within.$i.summary | awk '{print$2}' >> TdSorient.distance.tmp.A 
  grep TdStotal GIST.within.$i.summary | awk '{print$2}' >> TdStotal.distance.tmp.A 
  grep waters GIST.within.$i.summary | awk '{print$2}' >> waters.distance.tmp.A 
  echo $i
  @ i = i + 1 
  
end

paste distance.tmp.A Esw.distance.tmp.A > Esw.distance.dat
paste distance.tmp.A Eww.distance.tmp.A > Eww.distance.dat
paste distance.tmp.A dEww.distance.tmp.A > dEww.distance.dat
paste distance.tmp.A dEtot.distance.tmp.A > dEtot.distance.dat
paste distance.tmp.A TdStrans.distance.tmp.A > TdStrans.distance.dat
paste distance.tmp.A TdSorient.distance.tmp.A > TdSorient.distance.dat
paste distance.tmp.A TdStotal.distance.tmp.A > TdStotal.distance.dat
paste dEtot.distance.tmp.A TdStotal.distance.tmp.A | awk '{print$1-$2}' > dA.total.distance.tmp.A
paste distance.tmp.A dA.total.distance.tmp.A > dA.total.distance.dat
paste distance.tmp.A waters.distance.tmp.A > waters.distance.dat
rm *.tmp.A
