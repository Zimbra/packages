#!/bin/bash
awk 'BEGIN{FS="[:,]";OFS=","} /^Requires:/{ for(i=1;i<=NF;i++) { if($i ~ /zimbra-/) s=s ? s OFS $i : $i } if(s) print "Requires: "s; s="" } !/^Requires:/{print}' thirdparty/*/*/rpm/SPECS/*.spec
awk 'BEGIN{FS="[:,]";OFS=","} /^Requires:/{ for(i=1;i<=NF;i++) { if($i ~ /zimbra-/) s=s ? s OFS $i : $i } if(s) print "Requires: "s; s="" } !/^Requires:/{print}' zimbra/*/*/rpm/SPECS/*.spec
