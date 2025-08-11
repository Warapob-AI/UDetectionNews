# Starting from the given code
principle_list = [10000, #2003
                  10000, #2004
                  20000, #2005
                  30000, #2006
                  40000, #2007
                  50000, #2008
                  60000, #2009
                  70000, #2010
                  80000, #2011
                  90000, #2012
                  100000, #2013
                  100000, #2014
                  100000, #2015
                  100000, #2016
                  100000, #2017
                  100000, #2018
                  100000, #2019
                  100000, #2020
                  100000, #2021
                  100000, #2022
                  100000, #2023
                  100000] #2024

compound_perc_list = [
    -15.97, #2004
    6.79, #2005
    -16.53, #2006
    125.38, #2007
    -42.34, #2008
    162.89, #2009
    33.73, #2010
    -3.78, #2011
    49.65, #2012
    53.86, #2013
    -22.17, #2014
    117.72, #2015
    10.95, #2016
    55.96, #2017
    34.72, #2018
    17.29, #2019
    76.26, #2020
    2.38, #2021
    -49.62, #2022
    80.88, #2023
    44.39 ] #2024

start_year = 2003

total_value = 0 
total_initial_cost = 0  # Initialize the total initial cost

for i in range(len(principle_list)):
    principle_year = principle_list[i] * 12
    total_initial_cost += principle_year  # Add to the total initial cost
    test_principle = principle_year

    print(f"\n==== เงินลงทุนในปี {start_year + i} จำนวน {principle_year:,.2f} บาท ====")
    print(f"{start_year + i}: {test_principle:,.2f} บาท (เริ่มลงทุน)")

    for j in range(len(compound_perc_list) - i):
        compound = 1 + (compound_perc_list[i + j] / 100)
        test_principle *= compound
        print(f"{start_year + i + j + 1}: {test_principle:,.2f} บาท "
              f"(ผลตอบแทน {compound_perc_list[i + j]:+.2f}%)")

    print(f"→ มูลค่าปัจจุบันของเงินลงทุนปี {start_year + i}: {test_principle:,.2f} บาท ✅")
    total_value += test_principle  # รวมมูลค่าปัจจุบันของเงินแต่ละก้อน

# Summarize total current value
print("\n🎉 รวมมูลค่าปัจจุบันของเงินทั้งหมดจากทุกปี:", f"{total_value:,.2f} บาท")

# Print out the total initial investment
print(f"📊 ต้นทุนรวมที่ลงทุนทั้งหมด: {total_initial_cost:,.2f} บาท")