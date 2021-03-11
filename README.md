# PnP for JLCPCB

This application convert outputs from the Altium Designer to the JLCPCB format

## Script parameters

- `-i` or `--input` - input the pick and place file
  - Required: True
  
- `-b` or `--bom` - to modify `LCSC Part #` in BOM
  - Required: False
  
- `-r`, `--rotation` - to modify `Rotation` in P&P
  - Required: False
  
- `-o`, `--output` - to rename JLCPCB_xx.csv to output_xx.csv 
  - Required: False

## Example

```
python PnP_for_JLCPCB.py -i "PnP.csv" -b "Bom.csv" -r Crot.csv -o test
```

## Input files header format

###  PnP.csv

- The order of the names is not important.   
- All columns are required.   

```
"Designator","Comment","Layer","Footprint","Center-X(mm)","Center-Y(mm)","Rotation","Description"
```

or

```
Altium Designer Pick and Place Locations
c:\Path\xxx.csv

========================================================================================================================
File Design Information:

Date:       11.03.21
Time:       06:54
Revision:   Not in VersionControl
Variant:    No variations
Units used: mm

"Designator","Comment","Layer","Footprint","Center-X(mm)","Center-Y(mm)","Rotation","Description"
```

### BOM.csv

- The order of the names is not important.      
- Required columns are `Comment` and `LCSC Part #`.      

```
Comment,Description,Designator,Footprint,LibRef,Quantity,LCSC Part #
```


### Rotation.csv

- The order of the names is not important.   
- All columns are required.   
- `Correction` need to be in the range from -180 to 180 and in integer type.
- Only for the footprint you want to change.   

```
Footprint,Correction
```

