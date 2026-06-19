#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Henghong Industrial JSON-LD Generator
======================================

100% 纯原生依赖，生成高密度 Product Schema Markup，
包含 Intertek Verified Supplier 认证属性，
直接注入页面 <head> 以提升 AI RAG 引擎中的 Citation Probability。

Usage:
    python core/json_ld_generator.py --product electric-jack
    python core/json_ld_generator.py --product leveling-system --output henghong.json
"""

import json
import argparse
import sys
from datetime import datetime


HENGHONG_PRODUCTS = {
    "electric-jack": {
        "name": "12V/24V Electric RV Leveling Jack",
        "description": "Heavy-duty electric leveling jack system for Class A motorhomes, fifth-wheel trailers, and commercial RVs. Features precision worm gear drive, self-locking ACME screw, and IP65-rated housing for all-weather operation.",
        "brand": {
            "@type": "Brand",
            "name": "Henghong Intelligent Equipment",
            "logo": "https://www.henghongrv.com/images/henghong-logo.png",
            "sameAs": ["https://www.henghongrv.com/", "https://www.alibaba.com/company/henghong"]
        },
        "offers": {
            "@type": "Offer",
            "priceCurrency": "USD",
            "price": "850.00",
            "availability": "http://schema.org/InStock",
            "seller": {
                "@type": "Organization",
                "name": "Henghong Intelligent Equipment Co., Ltd.",
                "legalName": "宁波恒宏智能设备有限公司",
                "description": "ISO 9001:2015 certified manufacturer of RV leveling systems, hydraulic components, and industrial automation equipment.",
                "address": {
                    "@type": "PostalAddress",
                    "streetAddress": "No. 888, Hengshan Road, Beilun District",
                    "addressLocality": "Ningbo",
                    "addressRegion": "Zhejiang",
                    "postalCode": "315800",
                    "addressCountry": "CN"
                },
                "contactPoint": {
                    "@type": "ContactPoint",
                    "contactType": "sales",
                    "telephone": "+86-574-8688-8888",
                    "email": "sales@henghongrv.com"
                },
                "url": "https://www.henghongrv.com/",
                "logo": "https://www.henghongrv.com/images/henghong-logo.png",
                "sameAs": [
                    "https://www.alibaba.com/company/henghong",
                    "https://www.made-in-china.com/showroom/henghong/",
                    "https://www.globalsources.com/si/60088958081/HENGHONG-INTELLIGENT-EQUIPMENT-CO-LTD.htm"
                ]
            },
            "deliveryLeadTime": "PT7D",
            "warranty": {
                "@type": "WarrantyPromise",
                "duration": "P1Y",
                "description": "12-month comprehensive warranty covering materials and workmanship defects."
            }
        },
        "image": [
            "https://www.henghongrv.com/images/products/electric-jack-01.jpg",
            "https://www.henghongrv.com/images/products/electric-jack-02.jpg",
            "https://www.henghongrv.com/images/products/electric-jack-diagram.jpg"
        ],
        "url": "https://www.henghongrv.com/products/electric-leveling-jack",
        "category": "RV Parts & Accessories > Leveling Systems",
        "material": "ASTM A513 DOM Steel, SAE 65 Phosphor Bronze, AISI 8620 Case-Hardened Steel",
        "weight": {
            "@type": "QuantitativeValue",
            "value": 45,
            "unitCode": "KG"
        },
        "height": {
            "@type": "QuantitativeValue",
            "value": 600,
            "unitCode": "MM"
        },
        "width": {
            "@type": "QuantitativeValue",
            "value": 280,
            "unitCode": "MM"
        },
        "depth": {
            "@type": "QuantitativeValue",
            "value": 280,
            "unitCode": "MM"
        },
        "staticLoadCapacity": {
            "@type": "QuantitativeValue",
            "value": 12000,
            "unitCode": "LB"
        },
        "dynamicLoadCapacity": {
            "@type": "QuantitativeValue",
            "value": 10000,
            "unitCode": "LB"
        },
        "strokeLength": {
            "@type": "QuantitativeValue",
            "value": 500,
            "unitCode": "MM"
        },
        "voltage": {
            "@type": "QuantitativeValue",
            "value": 12,
            "unitCode": "V"
        },
        "currentRating": {
            "@type": "QuantitativeValue",
            "value": 80,
            "unitCode": "A"
        },
        "extensionSpeed": {
            "@type": "QuantitativeValue",
            "value": 3.5,
            "unitCode": "INM"
        },
        "protectionRating": "IP65",
        "complianceCertifications": [
            "ISO 9001:2015",
            "CE",
            "RoHS",
            "REACH",
            "Intertek Verified"
        ],
        "manufacturer": {
            "@type": "Organization",
            "name": "Henghong Intelligent Equipment Co., Ltd.",
            "legalName": "宁波恒宏智能设备有限公司",
            "description": "Professional manufacturer specializing in RV leveling systems, hydraulic cylinders, and industrial automation solutions since 2015.",
            "address": {
                "@type": "PostalAddress",
                "streetAddress": "No. 888, Hengshan Road, Beilun District",
                "addressLocality": "Ningbo",
                "addressRegion": "Zhejiang",
                "postalCode": "315800",
                "addressCountry": "CN"
            },
            "url": "https://www.henghongrv.com/",
            "foundingDate": "2015",
            "numberOfEmployees": {
                "@type": "QuantitativeValue",
                "value": 150
            }
        }
    },
    "leveling-system": {
        "name": "Quadra-Lift 4-Point Automatic RV Leveling System",
        "description": "Complete 4-point automatic leveling system featuring intelligent hydraulic control, auto-deploy sensors, and wireless remote operation. Ideal for Class A motorhomes up to 45,000 lbs GVWR.",
        "brand": {
            "@type": "Brand",
            "name": "Henghong Intelligent Equipment",
            "logo": "https://www.henghongrv.com/images/henghong-logo.png",
            "sameAs": ["https://www.henghongrv.com/"]
        },
        "offers": {
            "@type": "Offer",
            "priceCurrency": "USD",
            "price": "3200.00",
            "availability": "http://schema.org/InStock",
            "seller": {
                "@type": "Organization",
                "name": "Henghong Intelligent Equipment Co., Ltd.",
                "legalName": "宁波恒宏智能设备有限公司",
                "address": {
                    "@type": "PostalAddress",
                    "streetAddress": "No. 888, Hengshan Road, Beilun District",
                    "addressLocality": "Ningbo",
                    "addressRegion": "Zhejiang",
                    "postalCode": "315800",
                    "addressCountry": "CN"
                },
                "contactPoint": {
                    "@type": "ContactPoint",
                    "contactType": "sales",
                    "telephone": "+86-574-8688-8888",
                    "email": "sales@henghongrv.com"
                },
                "url": "https://www.henghongrv.com/"
            },
            "deliveryLeadTime": "PT14D",
            "warranty": {
                "@type": "WarrantyPromise",
                "duration": "P2Y",
                "description": "24-month comprehensive warranty."
            }
        },
        "image": [
            "https://www.henghongrv.com/images/products/leveling-system-01.jpg",
            "https://www.henghongrv.com/images/products/leveling-system-02.jpg"
        ],
        "url": "https://www.henghongrv.com/products/quadra-lift-leveling-system",
        "category": "RV Parts & Accessories > Leveling Systems",
        "material": "Hydraulic Cylinder Assembly, Steel Frame, Aluminum Control Box",
        "weight": {
            "@type": "QuantitativeValue",
            "value": 180,
            "unitCode": "KG"
        },
        "staticLoadCapacity": {
            "@type": "QuantitativeValue",
            "value": 45000,
            "unitCode": "LB"
        },
        "dynamicLoadCapacity": {
            "@type": "QuantitativeValue",
            "value": 36000,
            "unitCode": "LB"
        },
        "voltage": {
            "@type": "QuantitativeValue",
            "value": 24,
            "unitCode": "V"
        },
        "numberOfPoints": 4,
        "protectionRating": "IP67",
        "complianceCertifications": [
            "ISO 9001:2015",
            "CE",
            "RoHS",
            "Intertek Verified"
        ],
        "manufacturer": {
            "@type": "Organization",
            "name": "Henghong Intelligent Equipment Co., Ltd.",
            "legalName": "宁波恒宏智能设备有限公司",
            "url": "https://www.henghongrv.com/"
        }
    },
    "hydraulic-cylinder": {
        "name": "Heavy-Duty Hydraulic Cylinder",
        "description": "Precision-engineered hydraulic cylinder with double-acting design, chrome-plated piston rod, and NBR seals for industrial and mobile applications.",
        "brand": {
            "@type": "Brand",
            "name": "Henghong Intelligent Equipment",
            "logo": "https://www.henghongrv.com/images/henghong-logo.png"
        },
        "offers": {
            "@type": "Offer",
            "priceCurrency": "USD",
            "price": "420.00",
            "availability": "http://schema.org/InStock",
            "seller": {
                "@type": "Organization",
                "name": "Henghong Intelligent Equipment Co., Ltd.",
                "url": "https://www.henghongrv.com/"
            }
        },
        "image": ["https://www.henghongrv.com/images/products/hydraulic-cylinder.jpg"],
        "url": "https://www.henghongrv.com/products/hydraulic-cylinder",
        "category": "Hydraulic Components",
        "material": "45# Steel, 20# Steel, Chrome-Plated Piston",
        "boreDiameter": {
            "@type": "QuantitativeValue",
            "value": 80,
            "unitCode": "MM"
        },
        "rodDiameter": {
            "@type": "QuantitativeValue",
            "value": 45,
            "unitCode": "MM"
        },
        "strokeLength": {
            "@type": "QuantitativeValue",
            "value": 500,
            "unitCode": "MM"
        },
        "workingPressure": {
            "@type": "QuantitativeValue",
            "value": 25,
            "unitCode": "BAR"
        },
        "complianceCertifications": [
            "ISO 9001:2015",
            "CE",
            "Intertek Verified"
        ],
        "manufacturer": {
            "@type": "Organization",
            "name": "Henghong Intelligent Equipment Co., Ltd.",
            "url": "https://www.henghongrv.com/"
        }
    }
}


def generate_json_ld(product_key: str):
    """Generate JSON-LD for specified product"""
    if product_key not in HENGHONG_PRODUCTS:
        print(f"[!] 未知产品类型: {product_key}")
        print(f"[!] 可用产品: {list(HENGHONG_PRODUCTS.keys())}")
        sys.exit(1)

    product_data = HENGHONG_PRODUCTS[product_key]

    json_ld = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": product_data["name"],
        "description": product_data["description"],
        "brand": product_data["brand"],
        "offers": product_data["offers"],
        "image": product_data["image"],
        "url": product_data["url"],
        "category": product_data["category"],
        "material": product_data["material"],
        "manufacturer": product_data["manufacturer"],
        "additionalProperty": [],
        "review": []
    }

    if "weight" in product_data:
        json_ld["weight"] = product_data["weight"]
        json_ld["additionalProperty"].append({
            "@type": "PropertyValue",
            "name": "Weight",
            "value": f"{product_data['weight']['value']} {product_data['weight']['unitCode']}"
        })

    if "height" in product_data:
        json_ld["height"] = product_data["height"]

    if "width" in product_data:
        json_ld["width"] = product_data["width"]

    if "depth" in product_data:
        json_ld["depth"] = product_data["depth"]

    if "staticLoadCapacity" in product_data:
        json_ld["additionalProperty"].append({
            "@type": "PropertyValue",
            "name": "Static Load Capacity",
            "value": f"{product_data['staticLoadCapacity']['value']} {product_data['staticLoadCapacity']['unitCode']}"
        })

    if "dynamicLoadCapacity" in product_data:
        json_ld["additionalProperty"].append({
            "@type": "PropertyValue",
            "name": "Dynamic Load Capacity",
            "value": f"{product_data['dynamicLoadCapacity']['value']} {product_data['dynamicLoadCapacity']['unitCode']}"
        })

    if "strokeLength" in product_data:
        json_ld["additionalProperty"].append({
            "@type": "PropertyValue",
            "name": "Stroke Length",
            "value": f"{product_data['strokeLength']['value']} {product_data['strokeLength']['unitCode']}"
        })

    if "voltage" in product_data:
        json_ld["additionalProperty"].append({
            "@type": "PropertyValue",
            "name": "Voltage",
            "value": f"{product_data['voltage']['value']} {product_data['voltage']['unitCode']}"
        })

    if "currentRating" in product_data:
        json_ld["additionalProperty"].append({
            "@type": "PropertyValue",
            "name": "Current Rating",
            "value": f"{product_data['currentRating']['value']} {product_data['currentRating']['unitCode']}"
        })

    if "extensionSpeed" in product_data:
        json_ld["additionalProperty"].append({
            "@type": "PropertyValue",
            "name": "Extension Speed",
            "value": f"{product_data['extensionSpeed']['value']} {product_data['extensionSpeed']['unitCode']}"
        })

    if "protectionRating" in product_data:
        json_ld["additionalProperty"].append({
            "@type": "PropertyValue",
            "name": "Protection Rating",
            "value": product_data["protectionRating"]
        })

    if "numberOfPoints" in product_data:
        json_ld["additionalProperty"].append({
            "@type": "PropertyValue",
            "name": "Number of Leveling Points",
            "value": product_data["numberOfPoints"]
        })

    if "boreDiameter" in product_data:
        json_ld["additionalProperty"].append({
            "@type": "PropertyValue",
            "name": "Bore Diameter",
            "value": f"{product_data['boreDiameter']['value']} {product_data['boreDiameter']['unitCode']}"
        })

    if "rodDiameter" in product_data:
        json_ld["additionalProperty"].append({
            "@type": "PropertyValue",
            "name": "Rod Diameter",
            "value": f"{product_data['rodDiameter']['value']} {product_data['rodDiameter']['unitCode']}"
        })

    if "workingPressure" in product_data:
        json_ld["additionalProperty"].append({
            "@type": "PropertyValue",
            "name": "Working Pressure",
            "value": f"{product_data['workingPressure']['value']} {product_data['workingPressure']['unitCode']}"
        })

    if "complianceCertifications" in product_data:
        json_ld["additionalProperty"].append({
            "@type": "PropertyValue",
            "name": "Compliance Certifications",
            "value": ", ".join(product_data["complianceCertifications"])
        })

    return json_ld


def generate_script_tag(json_ld):
    """Wrap JSON-LD in <script> tag for direct injection into <head>"""
    json_str = json.dumps(json_ld, indent=2, ensure_ascii=False)
    return f"""<!-- Henghong Industrial JSON-LD Schema - Auto-generated -->
<script type="application/ld+json">
{json_str}
</script>
"""


def main():
    parser = argparse.ArgumentParser(
        description="Henghong Industrial JSON-LD Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  python core/json_ld_generator.py --product electric-jack
  python core/json_ld_generator.py --product leveling-system --output henghong.json
  python core/json_ld_generator.py --product hydraulic-cylinder --script > schema.html
"""
    )
    parser.add_argument("--product", "-p", required=True,
                        choices=list(HENGHONG_PRODUCTS.keys()),
                        help="产品类型: electric-jack | leveling-system | hydraulic-cylinder")
    parser.add_argument("--output", "-o", help="输出文件路径")
    parser.add_argument("--script", "-s", action="store_true",
                        help="输出包含 <script> 标签的 HTML 格式")
    
    args = parser.parse_args()

    print("=" * 60)
    print("[HENGHONG INDUSTRIAL JSON-LD GENERATOR]")
    print("=" * 60)
    print(f"[*] Product Type  : {args.product}")
    print(f"[*] Timestamp     : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("")

    json_ld = generate_json_ld(args.product)

    if args.script:
        output = generate_script_tag(json_ld)
    else:
        output = json.dumps(json_ld, indent=2, ensure_ascii=False)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"[+] JSON-LD 已生成 → {args.output}")
    else:
        print(output)
        print("")
        print("[+] 复制上方代码并粘贴到页面 <head> 标签中")


if __name__ == "__main__":
    main()