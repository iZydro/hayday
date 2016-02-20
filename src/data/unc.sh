ls -1 *.csv | while read f
do

	name=$f
	(
	dd if=$name bs=1 count=9
	dd if=/dev/zero bs=1 count=4
	dd if=$name bs=1 skip=9
	) | lzma -dc >$f.txt

done
