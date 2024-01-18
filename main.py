from typing import List
import pandas as pd
from bs4 import BeautifulSoup
from pyecharts.charts import Map, Page, Bar, Grid
from pyecharts import options as opts
import glob

province_dict = {
    1: '北京市',
    2: '天津市',
    3: '河北省',
    4: '山西省',
    5: '内蒙古自治区',
    6: '辽宁省',
    7: '吉林省',
    8: '黑龙江省',
    9: '上海市',
    10: '江苏省',
    11: '浙江省',
    12: '安徽省',
    13: '福建省',
    14: '江西省',
    15: '山东省',
    16: '河南省',
    17: '湖北省',
    18: '湖南省',
    19: '广东省',
    20: '广西壮族自治区',
    21: '海南省',
    22: '重庆市',
    23: '四川省',
    24: '贵州省',
    25: '云南省',
    26: '西藏自治区',
    27: '陕西省',
    28: '甘肃省',
    29: '青海省',
    30: '宁夏回族自治区',
    31: '新疆维吾尔自治区',
    32: '香港特别行政区',
    33: '澳门特别行政区',
    34: '台湾省',
}
hospital_data = []
province_list = []


def read_hot():
    dfs = []
    for i in range(1, 50):
        filelist: List[str] = glob.glob(
            "C:/Users/15251/IdeaProjects/MedicialAnalisy/src/main/resources/hospitalTop5/地区=" + str(i) + "/*.csv")
        if len(filelist) == 0:
            print("没有找到csv文件")
            continue
        df = pd.read_csv(filelist[0], encoding="utf-8")
        df['location'] = province_dict[i]
        dfs.append(df)
    result = pd.concat(dfs)
    return result


def read_location_csv(filename, colvalue):
    filelist: List[str] = glob.glob(
        "C:/Users/15251/IdeaProjects/MedicialAnalisy/src/main/resources/" + filename + "/*.csv")
    if filelist.count == 0:
        print("没有找到csv文件")
        exit()
    df = pd.read_csv(filelist[0], encoding="utf-8")
    df['location'] = df['location'].map(province_dict)
    return [list(z) for z in zip(df['location'].tolist(), df[colvalue].tolist())]


if __name__ == '__main__':
    # 就诊次数
    color_range1 = [
        {"min": 40, "color": "#751d0d"},
        {"min": 30, "max": 40, "color": "#d6564c"},
        {"min": 20, "max": 30, "color": "#f19178"},
        {"min": 10, "max": 20, "color": "#f7d3a6"},
        {"min": 1, "max": 9, "color": "#fdf2d3"},
        {"min": 0, "max": 0, "color": "#FFFFFF"}
    ]
    # 病人数量
    color_range2 = [
        {"min": 1000, "color": "#751d0d"},
        {"min": 800, "max": 1000, "color": "#d6564c"},
        {"min": 400, "max": 800, "color": "#f19178"},
        {"min": 200, "max": 400, "color": "#f7d3a6"},
        {"min": 1, "max": 200, "color": "#fdf2d3"},
        {"min": 0, "max": 0, "color": "#FFFFFF"}
    ]
    # 花费
    color_range3 = [
        {"min": 20000, "color": "#751d0d"},
        {"min": 15000, "max": 20000, "color": "#d6564c"},
        {"min": 10000, "max": 15000, "color": "#f19178"},
        {"min": 5000, "max": 10000, "color": "#f7d3a6"},
        {"min": 1, "max": 5000, "color": "#fdf2d3"},
        {"min": 0, "max": 0, "color": "#FFFFFF"}
    ]
    color_range4 = [
        {"min": 80, "color": "#751d0d"},
        {"min": 60, "max": 80, "color": "#d6564c"},
        {"min": 40, "max": 60, "color": "#f19178"},
        {"min": 20, "max": 40, "color": "#f7d3a6"},
        {"min": 1, "max": 20, "color": "#fdf2d3"},
        {"min": 0, "max": 0, "color": "#FFFFFF"}
    ]
    f_map = (
        Map(init_opts=opts.InitOpts(width="70%",
                                    height="700px",
                                    page_title="病人信息地图",
                                    ))
        .add(series_name="病人数量",
             data_pair=read_location_csv("patientCount", "sum"),
             maptype="china",
             is_map_symbol_show=False
             )

        .add(series_name="平均就诊次数",
             data_pair=read_location_csv("avgAllergy", "avg_Allergy"),
             maptype="china",
             is_map_symbol_show=False
             )
        .add(series_name="平均花费",
             data_pair=read_location_csv("avgExpend", "avg_expend"),
             maptype="china",
             is_map_symbol_show=False
             )
        .add(
            series_name="欺诈率(%)",
            data_pair=read_location_csv("deceptionRate","rate"),
            maptype="china",
            is_map_symbol_show=False
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="病人信息地图",
                                      subtitle="数据"
                                               "注：数据随机生成",
                                      pos_left="center", ),
            legend_opts=opts.LegendOpts(
                pos_left="left",
                selected_mode='single',
            ),
            visualmap_opts=[
                opts.VisualMapOpts(
                    is_piecewise=True,
                    range_text=['高', '低'],
                    pieces=color_range2,
                    pos_left='left'
                ),
            ],

        )
        .set_series_opts(label_opts=opts.LabelOpts(is_show=True),
                         markpoint_opts=opts.MarkPointOpts(
                             symbol_size=90, symbol='circle'),
                         effect_opts=opts.EffectOpts(is_show=True, )
                         )
    )

    f_map.chart_id = "patient_map"

    page = Page()
    page.add(f_map)
    page.add_js_funcs(
        """
            chart_patient_map.on('legendselectchanged', function (params) {
                var selected = params.selected;
                var color_range1 = %(color_range1)s;
                var color_range2 = %(color_range2)s;
                var color_range3 = %(color_range3)s;
                var color_range4 = %(color_range4)s;
                if (selected['平均就诊次数']) {
                    this.setOption({
                        visualMap: {
                            pieces: color_range1
                        }
                    });
                } else if(selected['病人数量']){
                    this.setOption({
                        visualMap: {
                            pieces: color_range2
                        }
                    });
                }  else if(selected['欺诈率(%%)']){
                    this.setOption({
                        visualMap: {
                            pieces: color_range4
                            
                        }
                    });
                } else{
                    this.setOption({
                        visualMap: {
                            pieces: color_range3
                        }
                    });
                }
            });
            """ % {'color_range1': color_range1, 'color_range2': color_range2, 'color_range3': color_range3,'color_range4':color_range4}
    )
    df = read_hot()
    bar = Bar(
        init_opts=opts.InitOpts(
            width="30%",  # 使用宽度的50%
            height="0px",

        )
    )
    bar.add_xaxis(df['医院编码_NN'].astype(str).tolist())
    bar.add_yaxis("人数", df['count'].tolist())
    bar.set_global_opts(
        title_opts={"text": "xx省患者最倾向于去的医院"},
        legend_opts=opts.LegendOpts(
            pos_left="right",
            selected_mode='single',
        ),
    )
    bar.set_series_opts()  # 初始时设置柱状图不可见
    bar.chart_id = "bar_chart"
    page.add(bar)
    js_code = """
var regionData = %s;  // 地区数据
var hospitalData = %s;  // 医院数据
var bar_chart = echarts.init(document.getElementById('bar_chart'));  // 获取柱状图实例

chart_patient_map.on('click', function(params) {
    // 获取点击的地区
    var selectedRegion = params.name;
    var newTitle=selectedRegion+"患者最倾向于去的医院";
    // 根据点击的地区获取对应的数据
    var indices = [];
    for (var i = 0; i < regionData.length; i++) {
        if (regionData[i] === selectedRegion) {
            indices.push(i);
        }
    }
    
    var newData = {
        '医院编码_NN': [],
        'count': []
    };
    
    for (var i = 0; i < indices.length; i++) {
        newData['医院编码_NN'].push(hospitalData['医院编码_NN'][indices[i]]+"医院");
        newData['count'].push(hospitalData['count'][indices[i]]);
    }
    bar_chart.resize({ height: "600px" });
        bar_chart.setOption({
            xAxis: {
                data: newData['医院编码_NN'].map(String)
            },
            series: [{
                data: newData['count']
            }],
            title: [{
                text: newTitle
            }],
            
        });
    });
    """ % (df['location'].tolist(), df[['医院编码_NN', 'count']].to_dict(orient='list'))
    page.add_js_funcs(js_code)
    page.render("map_page.html", encoding="utf-8")

    html_file_path = 'map_page.html'

    # 打开文件并读取内容
    with open(html_file_path, 'r', encoding='utf-8') as file:
        # 读取文件内容
        html_content = file.read()

    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # 查找样式标签并替换内容
    style_tag = soup.find('style', string=lambda text: ".box" in text if text else False)
    if style_tag:
        style_tag.string = ".box { display: flex; justify-content: space-around; }"

    # 保存修改后的HTML文件
    with open('map_page.html', 'w', encoding='utf-8') as file:
        file.write(str(soup))
