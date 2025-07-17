import json


def convert_flat_to_nested(nutrition_result):
    result = {"plan": []}
    plan_entries = nutrition_result["plan"]

    week_map = {}

    # Arabic to English meal type map
    meal_map = {
        "فطور": "breakfast",
        "غداء": "lunch",
        "عشاء": "dinner",
        "وجبة خفيفة": "snack"
    }

    for entry in plan_entries:
        week = entry["week"]
        day = entry["day"]
        meal_type = entry["meal_type"]

        # Create week if not exists
        if week not in week_map:
            week_obj = {"week": week, "days": []}
            week_map[week] = week_obj
            result["plan"].append(week_obj)

        week_obj = week_map[week]

        # Check if day already added
        day_obj = next((d for d in week_obj["days"] if d["day"] == day), None)
        if not day_obj:
            day_obj = {"day": day, "meals": {}}
            week_obj["days"].append(day_obj)

        # Add meal items
        ingredients = entry.get("ingredients", [])
        meal_items = []
        for item in ingredients:
            meal_items.append({
                "name": item.get("name", ""),
                "quantity": item.get("quantity", ""),
                "alternatives": {
                    "name": item.get("alternatives", {}).get("name", ""),
                    "quantity": item.get("alternatives", {}).get("quantity", "")
                }
            })

        day_obj["meals"][meal_type] = meal_items

    return result

plan= { "plan": [
                {
                    "week": "الأسبوع الأول",
                    "day": "اليوم الأول",
                    "meal_type": "فطور",
                    "ingredients": [
                        {
                            "name": "فول مدمس",
                            "quantity": "1.5 كوب مطبوخ",
                            "alternatives": {
                                "name": "بيض مسلوق",
                                "quantity": "3 بيضات"
                            }
                        },
                        {
                            "name": "خبز بلدي أسمر",
                            "quantity": "1 رغيف صغير",
                            "alternatives": {
                                "name": "خبز شعير",
                                "quantity": "1 رغيف صغير"
                            }
                        },
                        {
                            "name": "زيت زيتون",
                            "quantity": "1 ملعقة كبيرة",
                            "alternatives": {
                                "name": "زيتون أسود",
                                "quantity": "5 حبات"
                            }
                        },
                        {
                            "name": "طماطم",
                            "quantity": "1 حبة متوسطة",
                            "alternatives": {
                                "name": "خيار",
                                "quantity": "1 حبة"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الأول",
                    "day": "اليوم الأول",
                    "meal_type": "غداء",
                    "ingredients": [
                        {
                            "name": "صدور دجاج مشوية",
                            "quantity": "180 جرام",
                            "alternatives": {
                                "name": "سمك فيليه مشوي",
                                "quantity": "200 جرام"
                            }
                        },
                        {
                            "name": "أرز بني مطبوخ",
                            "quantity": "1.5 كوب",
                            "alternatives": {
                                "name": "أرز أبيض مطبوخ (كمية أقل)",
                                "quantity": "1 كوب"
                            }
                        },
                        {
                            "name": "سلطة خضراء مشكلة (خس، خيار، طماطم، فلفل)",
                            "quantity": "1 طبق كبير",
                            "alternatives": {
                                "name": "شوربة خضار",
                                "quantity": "1 طبق"
                            }
                        },
                        {
                            "name": "خضار سوتيه (كوسة، جزر، فاصوليا خضراء)",
                            "quantity": "1 كوب",
                            "alternatives": {
                                "name": "بروكلي مطبوخ",
                                "quantity": "1 كوب"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الأول",
                    "day": "اليوم الأول",
                    "meal_type": "وجبة خفيفة",
                    "ingredients": [
                        {
                            "name": "تفاحة متوسطة",
                            "quantity": "1 حبة",
                            "alternatives": {
                                "name": "زبادي يوناني قليل الدسم",
                                "quantity": "1 كوب"
                            }
                        },
                        {
                            "name": "عين جمل",
                            "quantity": "30 جرام",
                            "alternatives": {
                                "name": "لوز نيء",
                                "quantity": "30 جرام"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الأول",
                    "day": "اليوم الأول",
                    "meal_type": "عشاء",
                    "ingredients": [
                        {
                            "name": "جبنة قريش",
                            "quantity": "200 جرام",
                            "alternatives": {
                                "name": "تونا معلبة بالماء ومصفاة",
                                "quantity": "1 علبة صغيرة"
                            }
                        },
                        {
                            "name": "خس",
                            "quantity": "2 كوب",
                            "alternatives": {
                                "name": "خبز أسمر",
                                "quantity": "1 شريحة"
                            }
                        },
                        {
                            "name": "طماطم شيري",
                            "quantity": "1 كوب",
                            "alternatives": {
                                "name": "شرائح فلفل ملون",
                                "quantity": "1 كوب"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الأول",
                    "day": "اليوم الثاني",
                    "meal_type": "فطور",
                    "ingredients": [
                        {
                            "name": "بيض أومليت",
                            "quantity": "3 بيضات",
                            "alternatives": {
                                "name": "جبنة بيضاء قليلة الدسم",
                                "quantity": "100 جرام"
                            }
                        },
                        {
                            "name": "خبز قمح كامل",
                            "quantity": "2 شريحة",
                            "alternatives": {
                                "name": "خبز أسمر",
                                "quantity": "2 شريحة"
                            }
                        },
                        {
                            "name": "سبانخ طازجة",
                            "quantity": "1 كوب",
                            "alternatives": {
                                "name": "فلفل ألوان",
                                "quantity": "نصف حبة"
                            }
                        },
                        {
                            "name": "زبدة قليلة الدسم",
                            "quantity": "1 ملعقة صغيرة",
                            "alternatives": {
                                "name": "زيت زيتون",
                                "quantity": "1 ملعقة صغيرة"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الأول",
                    "day": "اليوم الثاني",
                    "meal_type": "غداء",
                    "ingredients": [
                        {
                            "name": "بطاطا حلوة مشوية",
                            "quantity": "1 حبة متوسطة (200 جرام)",
                            "alternatives": {
                                "name": "مكرونة قمح كامل",
                                "quantity": "1.5 كوب مطبوخ"
                            }
                        },
                        {
                            "name": "لحم بقري قليل الدهن (ستيك)",
                            "quantity": "150 جرام",
                            "alternatives": {
                                "name": "صدور دجاج مفرومة",
                                "quantity": "180 جرام"
                            }
                        },
                        {
                            "name": "سلطة جرجير وطماطم شيري",
                            "quantity": "1 طبق كبير",
                            "alternatives": {
                                "name": "فاصوليا خضراء مطبوخة",
                                "quantity": "1 كوب"
                            }
                        },
                        {
                            "name": "زيت زيتون",
                            "quantity": "1 ملعقة كبيرة",
                            "alternatives": {
                                "name": "زيتون",
                                "quantity": "5 حبات"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الأول",
                    "day": "اليوم الثاني",
                    "meal_type": "وجبة خفيفة",
                    "ingredients": [
                        {
                            "name": "برتقالة",
                            "quantity": "1 حبة متوسطة",
                            "alternatives": {
                                "name": "كمثرى",
                                "quantity": "1 حبة"
                            }
                        },
                        {
                            "name": "زبادي لايت",
                            "quantity": "1 كوب",
                            "alternatives": {
                                "name": "بذور الشيا",
                                "quantity": "1 ملعقة كبيرة"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الأول",
                    "day": "اليوم الثاني",
                    "meal_type": "عشاء",
                    "ingredients": [
                        {
                            "name": "شوربة عدس",
                            "quantity": "2 كوب",
                            "alternatives": {
                                "name": "دجاج مسلوق ومقطع",
                                "quantity": "150 جرام"
                            }
                        },
                        {
                            "name": "خبز محمص أسمر",
                            "quantity": "1 شريحة",
                            "alternatives": {
                                "name": "خبز أسمر",
                                "quantity": "1 شريحة"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الأول",
                    "day": "اليوم الثالث",
                    "meal_type": "فطور",
                    "ingredients": [
                        {
                            "name": "شوفان مطبوخ بالماء أو حليب قليل الدسم",
                            "quantity": "نصف كوب جاف",
                            "alternatives": {
                                "name": "حبوب إفطار كاملة مع حليب قليل الدسم",
                                "quantity": "1 كوب"
                            }
                        },
                        {
                            "name": "موز",
                            "quantity": "نصف حبة",
                            "alternatives": {
                                "name": "فراولة",
                                "quantity": "نصف كوب"
                            }
                        },
                        {
                            "name": "بذور شيا",
                            "quantity": "1 ملعقة كبيرة",
                            "alternatives": {
                                "name": "عين جمل",
                                "quantity": "15 جرام"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الأول",
                    "day": "اليوم الثالث",
                    "meal_type": "غداء",
                    "ingredients": [
                        {
                            "name": "سمك مشوي (مثل الماكريل)",
                            "quantity": "200 جرام",
                            "alternatives": {
                                "name": "دجاج مفروم",
                                "quantity": "180 جرام"
                            }
                        },
                        {
                            "name": "كينوا مطبوخة",
                            "quantity": "1 كوب",
                            "alternatives": {
                                "name": "أرز أسمر",
                                "quantity": "1 كوب مطبوخ"
                            }
                        },
                        {
                            "name": "سلطة تبولة (برغل قليل)",
                            "quantity": "1 طبق كبير",
                            "alternatives": {
                                "name": "سلطة ملفوف",
                                "quantity": "1 طبق كبير"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الأول",
                    "day": "اليوم الثالث",
                    "meal_type": "وجبة خفيفة",
                    "ingredients": [
                        {
                            "name": "خيار و جزر مقطع",
                            "quantity": "1 كوب",
                            "alternatives": {
                                "name": "عصير خضروات طازج",
                                "quantity": "1 كوب"
                            }
                        },
                        {
                            "name": "حمص الشام مسلوق",
                            "quantity": "نصف كوب",
                            "alternatives": {
                                "name": "زبادي يوناني",
                                "quantity": "1 كوب"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الأول",
                    "day": "اليوم الثالث",
                    "meal_type": "عشاء",
                    "ingredients": [
                        {
                            "name": "جبنة قريش",
                            "quantity": "150 جرام",
                            "alternatives": {
                                "name": "بيض مسلوق",
                                "quantity": "2 بيضة"
                            }
                        },
                        {
                            "name": "خضروات ورقية (خس، جرجير)",
                            "quantity": "2 كوب",
                            "alternatives": {
                                "name": "خبز أسمر",
                                "quantity": "1 شريحة"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الأول",
                    "day": "اليوم الرابع",
                    "meal_type": "فطور",
                    "ingredients": [
                        {
                            "name": "جبنة فيتا قليلة الدسم",
                            "quantity": "100 جرام",
                            "alternatives": {
                                "name": "فول مدمس",
                                "quantity": "1 كوب"
                            }
                        },
                        {
                            "name": "طماطم وخيار مقطع",
                            "quantity": "1 كوب",
                            "alternatives": {
                                "name": "خس",
                                "quantity": "1 كوب"
                            }
                        },
                        {
                            "name": "زيت حبة البركة",
                            "quantity": "1 ملعقة صغيرة",
                            "alternatives": {
                                "name": "زيت زيتون",
                                "quantity": "1 ملعقة صغيرة"
                            }
                        },
                        {
                            "name": "خبز قمح كامل",
                            "quantity": "1 شريحة",
                            "alternatives": {
                                "name": "خبز أسمر",
                                "quantity": "1 شريحة"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الأول",
                    "day": "اليوم الرابع",
                    "meal_type": "غداء",
                    "ingredients": [
                        {
                            "name": "كفتة مشوية (لحم بقري قليل الدهن)",
                            "quantity": "150 جرام",
                            "alternatives": {
                                "name": "لحم مفروم قليل الدهن",
                                "quantity": "150 جرام"
                            }
                        },
                        {
                            "name": "برغل مطبوخ",
                            "quantity": "1.5 كوب",
                            "alternatives": {
                                "name": "بطاطس مشوية",
                                "quantity": "1 حبة متوسطة"
                            }
                        },
                        {
                            "name": "سلطة فتوش",
                            "quantity": "1 طبق كبير",
                            "alternatives": {
                                "name": "سلطة بلدي",
                                "quantity": "1 طبق كبير"
                            }
                        },
                        {
                            "name": "بصل مشوي",
                            "quantity": "نصف حبة",
                            "alternatives": {
                                "name": "فلفل أخضر",
                                "quantity": "1 حبة"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الأول",
                    "day": "اليوم الرابع",
                    "meal_type": "وجبة خفيفة",
                    "ingredients": [
                        {
                            "name": "حفنة مكسرات مشكلة نيئة",
                            "quantity": "30 جرام",
                            "alternatives": {
                                "name": "زبادي لايت",
                                "quantity": "1 كوب"
                            }
                        },
                        {
                            "name": "موز",
                            "quantity": "نصف حبة",
                            "alternatives": {
                                "name": "جريب فروت",
                                "quantity": "نصف حبة"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الأول",
                    "day": "اليوم الرابع",
                    "meal_type": "عشاء",
                    "ingredients": [
                        {
                            "name": "سلطة تونة بالخضروات (تونا بالماء)",
                            "quantity": "1 علبة",
                            "alternatives": {
                                "name": "صدر دجاج مشوي مقطع",
                                "quantity": "150 جرام"
                            }
                        },
                        {
                            "name": "خس",
                            "quantity": "2 كوب",
                            "alternatives": {
                                "name": "خبز أسمر",
                                "quantity": "1 شريحة"
                            }
                        },
                        {
                            "name": "ذرة مسلوقة",
                            "quantity": "نصف كوب",
                            "alternatives": {
                                "name": "فلفل الوان",
                                "quantity": "نصف كوب"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الأول",
                    "day": "اليوم الخامس",
                    "meal_type": "فطور",
                    "ingredients": [
                        {
                            "name": "زبادي يوناني",
                            "quantity": "1 كوب",
                            "alternatives": {
                                "name": "لبنة قليلة الدسم",
                                "quantity": "100 جرام"
                            }
                        },
                        {
                            "name": "فواكه مشكلة (توت، فراولة)",
                            "quantity": "1 كوب",
                            "alternatives": {
                                "name": "جرانولا صحية",
                                "quantity": "ربع كوب"
                            }
                        },
                        {
                            "name": "عسل نحل",
                            "quantity": "1 ملعقة صغيرة",
                            "alternatives": {
                                "name": "خبز أسمر",
                                "quantity": "1 شريحة"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الأول",
                    "day": "اليوم الخامس",
                    "meal_type": "غداء",
                    "ingredients": [
                        {
                            "name": "بطاطس حلوة مطبوخة",
                            "quantity": "1 حبة متوسطة",
                            "alternatives": {
                                "name": "مكرونة قمح كامل",
                                "quantity": "1.5 كوب مطبوخ"
                            }
                        },
                        {
                            "name": "صدور دجاج مشوية",
                            "quantity": "180 جرام",
                            "alternatives": {
                                "name": "دجاج مفروم",
                                "quantity": "180 جرام"
                            }
                        },
                        {
                            "name": "سلطة ملفوف وجزر",
                            "quantity": "1 طبق كبير",
                            "alternatives": {
                                "name": "خضار سوتيه",
                                "quantity": "1 كوب"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الأول",
                    "day": "ال يوم الخامس",
                    "meal_type": "وجبة خفيفة",
                    "ingredients": [
                        {
                            "name": "موز",
                            "quantity": "1 حبة متوسطة",
                            "alternatives": {
                                "name": "زبدة الفول السوداني الطبيعية",
                                "quantity": "1 ملعقة كبيرة"
                            }
                        },
                        {
                            "name": "كوب حليب قليل الدسم",
                            "quantity": "1 كوب",
                            "alternatives": {
                                "name": "زبادي طبيعي",
                                "quantity": "1 كوب"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الأول",
                    "day": "اليوم الخامس",
                    "meal_type": "عشاء",
                    "ingredients": [
                        {
                            "name": "شوربة عدس",
                            "quantity": "2 كوب",
                            "alternatives": {
                                "name": "شوربة دجاج بالخضار",
                                "quantity": "2 كوب"
                            }
                        },
                        {
                            "name": "بقدونس مفروم",
                            "quantity": "2 ملعقة كبيرة",
                            "alternatives": {
                                "name": "خبز أسمر",
                                "quantity": "1 شريحة"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الأول",
                    "day": "اليوم السادس",
                    "meal_type": "فطور",
                    "ingredients": [
                        {
                            "name": "فول مدمس",
                            "quantity": "1.5 كوب مطبوخ",
                            "alternatives": {
                                "name": "أومليت بيض مع خضروات",
                                "quantity": "3 بيضات"
                            }
                        },
                        {
                            "name": "خبز أسمر",
                            "quantity": "1 رغيف صغير",
                            "alternatives": {
                                "name": "خبز شوفان",
                                "quantity": "1 رغيف صغير"
                            }
                        },
                        {
                            "name": "طماطم وخيار",
                            "quantity": "1 كوب",
                            "alternatives": {
                                "name": "جرجير",
                                "quantity": "1 كوب"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الأول",
                    "day": "اليوم السادس",
                    "meal_type": "غداء",
                    "ingredients": [
                        {
                            "name": "صدور دجاج مشوية",
                            "quantity": "180 جرام",
                            "alternatives": {
                                "name": "سمك بلطي مشوي",
                                "quantity": "200 جرام"
                            }
                        },
                        {
                            "name": "مكرونة قمح كامل",
                            "quantity": "1.5 كوب مطبوخ",
                            "alternatives": {
                                "name": "أرز بني",
                                "quantity": "1.5 كوب مطبوخ"
                            }
                        },
                        {
                            "name": "سلطة خضراء كبيرة",
                            "quantity": "1 طبق كبير",
                            "alternatives": {
                                "name": "خضار سوتيه",
                                "quantity": "1 كوب"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الأول",
                    "day": "اليوم السادس",
                    "meal_type": "وجبة خفيفة",
                    "ingredients": [
                        {
                            "name": "زبادي يوناني",
                            "quantity": "1 كوب",
                            "alternatives": {
                                "name": "بيض مسلوق",
                                "quantity": "2 بيضة"
                            }
                        },
                        {
                            "name": "مكسرات مشكلة نيئة",
                            "quantity": "30 جرام",
                            "alternatives": {
                                "name": "بذور اليقطين",
                                "quantity": "20 جرام"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الأول",
                    "day": "اليوم السادس",
                    "meal_type": "عشاء",
                    "ingredients": [
                        {
                            "name": "سلطة تونة (معلبة بالماء)",
                            "quantity": "1 علبة",
                            "alternatives": {
                                "name": "سلطة جبنة قريش",
                                "quantity": "150 جرام"
                            }
                        },
                        {
                            "name": "خس وطماطم وخيار",
                            "quantity": "2 كوب",
                            "alternatives": {
                                "name": "فلفل الوان",
                                "quantity": "نصف كوب"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الأول",
                    "day": "اليوم السابع",
                    "meal_type": "فطور",
                    "ingredients": [
                        {
                            "name": "بيض مسلوق",
                            "quantity": "3 بيضات",
                            "alternatives": {
                                "name": "شوفان بالحليب والمكسرات",
                                "quantity": "نصف كوب شوفان"
                            }
                        },
                        {
                            "name": "خضروات ورقية",
                            "quantity": "1 كوب",
                            "alternatives": {
                                "name": "زيتون",
                                "quantity": "5 حبات"
                            }
                        },
                        {
                            "name": "جبنة بيضاء قليلة الدسم",
                            "quantity": "100 جرام",
                            "alternatives": {
                                "name": "خبز أسمر",
                                "quantity": "1 شريحة"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الأول",
                    "day": "اليوم السابع",
                    "meal_type": "غداء",
                    "ingredients": [
                        {
                            "name": "صدور دجاج مشوية",
                            "quantity": "180 جرام",
                            "alternatives": {
                                "name": "لحم بتلو مشوي",
                                "quantity": "150 جرام"
                            }
                        },
                        {
                            "name": "أرز بني",
                            "quantity": "1.5 كوب مطبوخ",
                            "alternatives": {
                                "name": "فريكة مطبوخة",
                                "quantity": "1 كوب"
                            }
                        },
                        {
                            "name": "سلطة كينوا",
                            "quantity": "1 طبق كبير",
                            "alternatives": {
                                "name": "بروكلي مسلوق",
                                "quantity": "1 كوب"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الأول",
                    "day": "اليوم السابع",
                    "meal_type": "وجبة خفيفة",
                    "ingredients": [
                        {
                            "name": "فراولة",
                            "quantity": "1 كوب",
                            "alternatives": {
                                "name": "عصير برتقال طبيعي (غير محلى)",
                                "quantity": "1 كوب"
                            }
                        },
                        {
                            "name": "زبادي لايت",
                            "quantity": "1 كوب",
                            "alternatives": {
                                "name": "لوز نيء",
                                "quantity": "20 جرام"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الأول",
                    "day": "اليوم السابع",
                    "meal_type": "عشاء",
                    "ingredients": [
                        {
                            "name": "عدس بجبة مطبوخ",
                            "quantity": "1.5 كوب",
                            "alternatives": {
                                "name": "شوربة خضار",
                                "quantity": "2 كوب"
                            }
                        },
                        {
                            "name": "بصل أخضر",
                            "quantity": "1 عود",
                            "alternatives": {
                                "name": "خبز أسمر",
                                "quantity": "1 شريحة"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الثاني",
                    "day": "اليوم الأول",
                    "meal_type": "فطور",
                    "ingredients": [
                        {
                            "name": "فول مدمس",
                            "quantity": "1.5 كوب مطبوخ",
                            "alternatives": {
                                "name": "بيض مسلوق",
                                "quantity": "3 بيضات"
                            }
                        },
                        {
                            "name": "زيت بذرة الكتان",
                            "quantity": "1 ملعقة كبيرة",
                            "alternatives": {
                                "name": "زيت زيتون",
                                "quantity": "1 ملعقة كبيرة"
                            }
                        },
                        {
                            "name": "خبز بلدي أسمر",
                            "quantity": "1 رغيف صغير",
                            "alternatives": {
                                "name": "خبز شعير",
                                "quantity": "1 رغيف صغير"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الثاني",
                    "day": "اليوم الأول",
                    "meal_type": "غداء",
                    "ingredients": [
                        {
                            "name": "دجاج مشوي",
                            "quantity": "180 جرام",
                            "alternatives": {
                                "name": "سمك ماكريل مشوي",
                                "quantity": "200 جرام"
                            }
                        },
                        {
                            "name": "كينوا مطبوخة",
                            "quantity": "1.5 كوب",
                            "alternatives": {
                                "name": "بطاطس مشوية",
                                "quantity": "1 حبة متوسطة"
                            }
                        },
                        {
                            "name": "سلطة فتوش",
                            "quantity": "1 طبق كبير",
                            "alternatives": {
                                "name": "سلطة جرجير وباذنجان مشوي",
                                "quantity": "1 طبق كبير"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الثاني",
                    "day": "اليوم الأول",
                    "meal_type": "وجبة خفيفة",
                    "ingredients": [
                        {
                            "name": "موز",
                            "quantity": "1 حبة",
                            "alternatives": {
                                "name": "زبادي بالبذور",
                                "quantity": "1 كوب"
                            }
                        },
                        {
                            "name": "لوز نيء",
                            "quantity": "30 جرام",
                            "alternatives": {
                                "name": "عين جمل",
                                "quantity": "30 جرام"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الثاني",
                    "day": "اليوم الأول",
                    "meal_type": "عشاء",
                    "ingredients": [
                        {
                            "name": "جبنة قريش",
                            "quantity": "200 جرام",
                            "alternatives": {
                                "name": "شرائح ديك رومي مدخن قليل الدسم",
                                "quantity": "100 جرام"
                            }
                        },
                        {
                            "name": "خس",
                            "quantity": "2 كوب",
                            "alternatives": {
                                "name": "خبز أسمر",
                                "quantity": "1 شريحة"
                            }
                        },
                        {
                            "name": "فلفل الوان",
                            "quantity": "نصف كوب",
                            "alternatives": {
                                "name": "خيار",
                                "quantity": "1 حبة"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الثاني",
                    "day": "اليوم الثاني",
                    "meal_type": "فطور",
                    "ingredients": [
                        {
                            "name": "بيض أومليت بالسبانخ والفطر",
                            "quantity": "3 بيضات",
                            "alternatives": {
                                "name": "شوفان بالفاكهة",
                                "quantity": "نصف كوب جاف"
                            }
                        },
                        {
                            "name": "خبز قمح كامل",
                            "quantity": "2 شريحة",
                            "alternatives": {
                                "name": "خبز أسمر",
                                "quantity": "2 شريحة"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الثاني",
                    "day": "اليوم الثاني",
                    "meal_type": "غداء",
                    "ingredients": [
                        {
                            "name": "سمك مشوي (سالمون)",
                            "quantity": "180 جرام",
                            "alternatives": {
                                "name": "لحم مفروم قليل الدهن",
                                "quantity": "150 جرام"
                            }
                        },
                        {
                            "name": "مكرونة قمح كامل",
                            "quantity": "1.5 كوب مطبوخ",
                            "alternatives": {
                                "name": "أرز بني",
                                "quantity": "1.5 كوب مطبوخ"
                            }
                        },
                        {
                            "name": "خضار سوتيه",
                            "quantity": "1 كوب",
                            "alternatives": {
                                "name": "سلطة خضراء",
                                "quantity": "1 طبق كبير"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الثاني",
                    "day": "اليوم الثاني",
                    "meal_type": "وجبة خفيفة",
                    "ingredients": [
                        {
                            "name": "زبادي يوناني",
                            "quantity": "1 كوب",
                            "alternatives": {
                                "name": "فراولة",
                                "quantity": "1 كوب"
                            }
                        },
                        {
                            "name": "بذور الشيا",
                            "quantity": "1 ملعقة كبيرة",
                            "alternatives": {
                                "name": "عسل نحل",
                                "quantity": "1 ملعقة صغيرة"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الثاني",
                    "day": "اليوم الثاني",
                    "meal_type": "عشاء",
                    "ingredients": [
                        {
                            "name": "شوربة بروكلي بالدجاج",
                            "quantity": "2 كوب",
                            "alternatives": {
                                "name": "سلطة تونا بالخضار",
                                "quantity": "1 علبة"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الثاني",
                    "day": "اليوم الثالث",
                    "meal_type": "فطور",
                    "ingredients": [
                        {
                            "name": "فول مدمس بالبيض",
                            "quantity": "1.5 كوب مطبوخ",
                            "alternatives": {
                                "name": "زبادي يوناني مع فواكه",
                                "quantity": "1 كوب زبادي"
                            }
                        },
                        {
                            "name": "خبز شوفان",
                            "quantity": "1 رغيف صغير",
                            "alternatives": {
                                "name": "خبز أسمر",
                                "quantity": "1 رغيف صغير"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الثاني",
                    "day": "اليوم الثالث",
                    "meal_type": "غداء",
                    "ingredients": [
                        {
                            "name": "صينية خضار بالدجاج (بطاطس، كوسة، جزر)",
                            "quantity": "200 جرام دجاج + 2 كوب خضار",
                            "alternatives": {
                                "name": "مكرونة قمح كامل بالدجاج والخضار",
                                "quantity": "1.5 كوب مطبوخ"
                            }
                        },
                        {
                            "name": "خبز أسمر",
                            "quantity": "1 شريحة",
                            "alternatives": {
                                "name": "أرز بني",
                                "quantity": "1 كوب مطبوخ"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الثاني",
                    "day": "اليوم الثالث",
                    "meal_type": "وجبة خفيفة",
                    "ingredients": [
                        {
                            "name": "حمص الشام مسلوق",
                            "quantity": "نصف كوب",
                            "alternatives": {
                                "name": "مكسرات مشكلة",
                                "quantity": "30 جرام"
                            }
                        },
                        {
                            "name": "جزر",
                            "quantity": "1 حبة",
                            "alternatives": {
                                "name": "خيار",
                                "quantity": "1 حبة"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الثاني",
                    "day": "اليوم الثالث",
                    "meal_type": "عشاء",
                    "ingredients": [
                        {
                            "name": "سلطة جبنة قريش وخضروات",
                            "quantity": "150 جرام جبنة + 2 كوب خضار",
                            "alternatives": {
                                "name": "شوربة عدس",
                                "quantity": "2 كوب"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الثاني",
                    "day": "اليوم الرابع",
                    "meal_type": "فطور",
                    "ingredients": [
                        {
                            "name": "بيض مسلوق",
                            "quantity": "3 بيضات",
                            "alternatives": {
                                "name": "جبنة بيضاء قليلة الدسم",
                                "quantity": "100 جرام"
                            }
                        },
                        {
                            "name": "خيار وفلفل ألوان",
                            "quantity": "1 كوب",
                            "alternatives": {
                                "name": "خس وطماطم",
                                "quantity": "1 كوب"
                            }
                        },
                        {
                            "name": "خبز قمح كامل",
                            "quantity": "1 شريحة",
                            "alternatives": {
                                "name": "خبز أسمر",
                                "quantity": "1 شريحة"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الثاني",
                    "day": "اليوم الرابع",
                    "meal_type": "غداء",
                    "ingredients": [
                        {
                            "name": "لحم مفروم بالخضار",
                            "quantity": "150 جرام لحم + 2 كوب خضار",
                            "alternatives": {
                                "name": "دجاج بالخضار في الفرن",
                                "quantity": "180 جرام دجاج + 2 كوب خضار"
                            }
                        },
                        {
                            "name": "بطاطا حلوة مشوية",
                            "quantity": "1 حبة متوسطة",
                            "alternatives": {
                                "name": "أرز بني",
                                "quantity": "1.5 كوب مطبوخ"
                            }
                        },
                        {
                            "name": "سلطة كولسلو دايت",
                            "quantity": "1 طبق كبير",
                            "alternatives": {
                                "name": "سلطة بلدي",
                                "quantity": "1 طبق كبير"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الثاني",
                    "day": "اليوم الرابع",
                    "meal_type": "وجبة خفيفة",
                    "ingredients": [
                        {
                            "name": "كمثرى",
                            "quantity": "1 حبة متوسطة",
                            "alternatives": {
                                "name": "تفاح",
                                "quantity": "1 حبة"
                            }
                        },
                        {
                            "name": "حليب قليل الدسم",
                            "quantity": "1 كوب",
                            "alternatives": {
                                "name": "زبادي يوناني",
                                "quantity": "1 كوب"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الثاني",
                    "day": "اليوم الرابع",
                    "meal_type": "عشاء",
                    "ingredients": [
                        {
                            "name": "سلطة تونا بالخضروات",
                            "quantity": "1 علبة تونا + 2 كوب خضار",
                            "alternatives": {
                                "name": "سلطة دجاج مشوي",
                                "quantity": "150 جرام دجاج + 2 كوب خضار"
                            }
                        },
                        {
                            "name": "أفوكادو (للطاقة)",
                            "quantity": "نصف حبة",
                            "alternatives": {
                                "name": "خبز أسمر",
                                "quantity": "1 شريحة"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الثاني",
                    "day": "اليوم الخامس",
                    "meal_type": "فطور",
                    "ingredients": [
                        {
                            "name": "جبنة قريش بالعسل والمكسرات",
                            "quantity": "150 جرام جبنة + 1 ملعقة عسل + 20 جرام مكسرات",
                            "alternatives": {
                                "name": "شوفان بالفاكهة",
                                "quantity": "نصف كوب جاف"
                            }
                        },
                        {
                            "name": "شرائح تفاح",
                            "quantity": "نصف حبة",
                            "alternatives": {
                                "name": "خبز أسمر",
                                "quantity": "1 شريحة"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الثاني",
                    "day": "اليوم الخامس",
                    "meal_type": "غداء",
                    "ingredients": [
                        {
                            "name": "صدور دجاج بصوص الليمون",
                            "quantity": "180 جرام",
                            "alternatives": {
                                "name": "سمك مشوي (بلطي)",
                                "quantity": "200 جرام"
                            }
                        },
                        {
                            "name": "برغل مطبوخ",
                            "quantity": "1.5 كوب",
                            "alternatives": {
                                "name": "أرز بني",
                                "quantity": "1.5 كوب مطبوخ"
                            }
                        },
                        {
                            "name": "خضار سوتيه",
                            "quantity": "1 كوب",
                            "alternatives": {
                                "name": "سلطة خضراء",
                                "quantity": "1 طبق كبير"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الثاني",
                    "day": "اليوم الخامس",
                    "meal_type": "وجبة خفيفة",
                    "ingredients": [
                        {
                            "name": "فراولة",
                            "quantity": "1 كوب",
                            "alternatives": {
                                "name": "زبادي يوناني",
                                "quantity": "1 كوب"
                            }
                        },
                        {
                            "name": "بذور الشيا",
                            "quantity": "1 ملعقة كبيرة",
                            "alternatives": {
                                "name": "بذور الكتان",
                                "quantity": "1 ملعقة كبيرة"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الثاني",
                    "day": "اليوم الخامس",
                    "meal_type": "عشاء",
                    "ingredients": [
                        {
                            "name": "شوربة خضار",
                            "quantity": "2 كوب",
                            "alternatives": {
                                "name": "شوربة عدس",
                                "quantity": "2 كوب"
                            }
                        },
                        {
                            "name": "كزبرة خضراء",
                            "quantity": "2 ملعقة كبيرة",
                            "alternatives": {
                                "name": "خبز أسمر",
                                "quantity": "1 شريحة"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الثاني",
                    "day": "اليوم السادس",
                    "meal_type": "فطور",
                    "ingredients": [
                        {
                            "name": "أومليت بيض بالجبنة قليلة الدسم",
                            "quantity": "3 بيضات + 50 جرام جبنة",
                            "alternatives": {
                                "name": "فول بالخضراوات",
                                "quantity": "1.5 كوب مطبوخ"
                            }
                        },
                        {
                            "name": "خبز قمح كامل",
                            "quantity": "1 رغيف صغير",
                            "alternatives": {
                                "name": "خبز أسمر",
                                "quantity": "1 رغيف صغير"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الثاني",
                    "day": "اليوم السادس",
                    "meal_type": "غداء",
                    "ingredients": [
                        {
                            "name": "لحم مشوي",
                            "quantity": "150 جرام",
                            "alternatives": {
                                "name": "كفتة دجاج مشوية",
                                "quantity": "180 جرام"
                            }
                        },
                        {
                            "name": "بطاطا حلوة مشوية",
                            "quantity": "1 حبة متوسطة",
                            "alternatives": {
                                "name": "أرز بسمتي أسمر",
                                "quantity": "1.5 كوب مطبوخ"
                            }
                        },
                        {
                            "name": "خضار سوتيه",
                            "quantity": "1 كوب",
                            "alternatives": {
                                "name": "سلطة جزر وبقدونس",
                                "quantity": "1 طبق كبير"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الثاني",
                    "day": "اليوم السادس",
                    "meal_type": "وجبة خفيفة",
                    "ingredients": [
                        {
                            "name": "تفاح",
                            "quantity": "1 حبة متوسطة",
                            "alternatives": {
                                "name": "موز",
                                "quantity": "1 حبة"
                            }
                        },
                        {
                            "name": "بذور اليقطين",
                            "quantity": "20 جرام",
                            "alternatives": {
                                "name": "مكسرات مشكلة",
                                "quantity": "30 جرام"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الثاني",
                    "day": "اليوم السادس",
                    "meal_type": "عشاء",
                    "ingredients": [
                        {
                            "name": "سلطة جبنة قريش",
                            "quantity": "150 جرام جبنة",
                            "alternatives": {
                                "name": "زبادي يوناني",
                                "quantity": "1 كوب"
                            }
                        },
                        {
                            "name": "طماطم",
                            "quantity": "1 حبة متوسطة",
                            "alternatives": {
                                "name": "خيار",
                                "quantity": "1 حبة"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الثاني",
                    "day": "اليوم السابع",
                    "meal_type": "فطور",
                    "ingredients": [
                        {
                            "name": "فول مدمس",
                            "quantity": "1.5 كوب مطبوخ",
                            "alternatives": {
                                "name": "بيض مسلوق",
                                "quantity": "3 بيضات"
                            }
                        },
                        {
                            "name": "خيار",
                            "quantity": "1 حبة",
                            "alternatives": {
                                "name": "طماطم",
                                "quantity": "1 حبة متوسطة"
                            }
                        },
                        {
                            "name": "خبز شعير",
                            "quantity": "1 رغيف صغير",
                            "alternatives": {
                                "name": "خبز أسمر",
                                "quantity": "1 رغيف صغير"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الثاني",
                    "day": "اليوم السابع",
                    "meal_type": "غداء",
                    "ingredients": [
                        {
                            "name": "سمك مشوي (قشر بياض)",
                            "quantity": "200 جرام",
                            "alternatives": {
                                "name": "صدور دجاج مشوية",
                                "quantity": "180 جرام"
                            }
                        },
                        {
                            "name": "أرز بني",
                            "quantity": "1.5 كوب مطبوخ",
                            "alternatives": {
                                "name": "مكرونة قمح كامل",
                                "quantity": "1.5 كوب مطبوخ"
                            }
                        },
                        {
                            "name": "شوربة لسان عصفور أسمر (خفيف)",
                            "quantity": "1 طبق",
                            "alternatives": {
                                "name": "سلطة بلدي",
                                "quantity": "1 طبق كبير"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الثاني",
                    "day": "اليوم السابع",
                    "meal_type": "وجبة خفيفة",
                    "ingredients": [
                        {
                            "name": "فواكه مشكلة",
                            "quantity": "1 كوب",
                            "alternatives": {
                                "name": "زبادي يوناني",
                                "quantity": "1 كوب"
                            }
                        },
                        {
                            "name": "بذور الكتان",
                            "quantity": "1 ملعقة كبيرة",
                            "alternatives": {
                                "name": "لوز نيء",
                                "quantity": "20 جرام"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الثاني",
                    "day": "اليوم السابع",
                    "meal_type": "عشاء",
                    "ingredients": [
                        {
                            "name": "شوربة كريمة الدجاج (قليلة الدسم)",
                            "quantity": "2 كوب",
                            "alternatives": {
                                "name": "شوربة عدس",
                                "quantity": "2 كوب"
                            }
                        },
                        {
                            "name": "بصل أخضر",
                            "quantity": "1 عود",
                            "alternatives": {
                                "name": "خبز أسمر",
                                "quantity": "1 شريحة"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الثالث",
                    "day": "اليوم الأول",
                    "meal_type": "فطور",
                    "ingredients": [
                        {
                            "name": "فول مدمس",
                            "quantity": "1.5 كوب مطبوخ",
                            "alternatives": {
                                "name": "بيض مسلوق",
                                "quantity": "3 بيضات"
                            }
                        },
                        {
                            "name": "طحينة قليلة الملح",
                            "quantity": "1 ملعقة كبيرة",
                            "alternatives": {
                                "name": "زيت زيتون",
                                "quantity": "1 ملعقة كبيرة"
                            }
                        },
                        {
                            "name": "خبز بلدي أسمر",
                            "quantity": "1 رغيف صغير",
                            "alternatives": {
                                "name": "خبز شوفان",
                                "quantity": "1 رغيف صغير"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الثالث",
                    "day": "اليوم الأول",
                    "meal_type": "غداء",
                    "ingredients": [
                        {
                            "name": "صدور دجاج مشوية بالزعتر",
                            "quantity": "180 جرام",
                            "alternatives": {
                                "name": "سمك فيليه مشوي",
                                "quantity": "200 جرام"
                            }
                        },
                        {
                            "name": "أرز بني مطبوخ",
                            "quantity": "1.5 كوب",
                            "alternatives": {
                                "name": "كينوا مطبوخة",
                                "quantity": "1.5 كوب"
                            }
                        },
                        {
                            "name": "خضار سوتيه",
                            "quantity": "1 كوب",
                            "alternatives": {
                                "name": "سلطة بروكلي وذرة",
                                "quantity": "1 طبق كبير"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الثالث",
                    "day": "اليوم الأول",
                    "meal_type": "وجبة خفيفة",
                    "ingredients": [
                        {
                            "name": "تفاح",
                            "quantity": "1 حبة متوسطة",
                            "alternatives": {
                                "name": "زبادي يوناني",
                                "quantity": "1 كوب"
                            }
                        },
                        {
                            "name": "عين جمل",
                            "quantity": "30 جرام",
                            "alternatives": {
                                "name": "لوز نيء",
                                "quantity": "30 جرام"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الثالث",
                    "day": "اليوم الأول",
                    "meal_type": "عشاء",
                    "ingredients": [
                        {
                            "name": "جبنة قريش",
                            "quantity": "200 جرام",
                            "alternatives": {
                                "name": "تونا معلبة بالماء ومصفاة",
                                "quantity": "1 علبة صغيرة"
                            }
                        },
                        {
                            "name": "خس",
                            "quantity": "2 كوب",
                            "alternatives": {
                                "name": "خيار",
                                "quantity": "1 حبة"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الثالث",
                    "day": "اليوم الثاني",
                    "meal_type": "فطور",
                    "ingredients": [
                        {
                            "name": "بيض أومليت بالفلفل الألوان",
                            "quantity": "3 بيضات",
                            "alternatives": {
                                "name": "جبنة بيضاء قليلة الدسم",
                                "quantity": "100 جرام"
                            }
                        },
                        {
                            "name": "خبز أسمر",
                            "quantity": "2 شريحة",
                            "alternatives": {
                                "name": "خبز قمح كامل",
                                "quantity": "2 شريحة"
                            }
                        },
                        {
                            "name": "فلفل ألوان",
                            "quantity": "نصف حبة",
                            "alternatives": {
                                "name": "طماطم",
                                "quantity": "1 حبة متوسطة"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الثالث",
                    "day": "اليوم الثاني",
                    "meal_type": "غداء",
                    "ingredients": [
                        {
                            "name": "لحم بقري مشوي",
                            "quantity": "150 جرام",
                            "alternatives": {
                                "name": "سمك بلطي مشوي",
                                "quantity": "200 جرام"
                            }
                        },
                        {
                            "name": "بطاطس مشوية",
                            "quantity": "1 حبة متوسطة",
                            "alternatives": {
                                "name": "مكرونة قمح كامل بصوص الطماطم",
                                "quantity": "1.5 كوب مطبوخ"
                            }
                        },
                        {
                            "name": "خضار سوتيه",
                            "quantity": "1 كوب",
                            "alternatives": {
                                "name": "سلطة فاصوليا خضراء",
                                "quantity": "1 طبق كبير"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الثالث",
                    "day": "اليوم الثاني",
                    "meal_type": "وجبة خفيفة",
                    "ingredients": [
                        {
                            "name": "كمثرى",
                            "quantity": "1 حبة متوسطة",
                            "alternatives": {
                                "name": "برتقالة",
                                "quantity": "1 حبة"
                            }
                        },
                        {
                            "name": "زبادي لايت",
                            "quantity": "1 كوب",
                            "alternatives": {
                                "name": "بذور الشيا",
                                "quantity": "1 ملعقة كبيرة"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الثالث",
                    "day": "اليوم الثاني",
                    "meal_type": "عشاء",
                    "ingredients": [
                        {
                            "name": "شوربة خضار بالدجاج",
                            "quantity": "2 كوب",
                            "alternatives": {
                                "name": "شوربة عدس",
                                "quantity": "2 كوب"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الثالث",
                    "day": "اليوم الثالث",
                    "meal_type": "فطور",
                    "ingredients": [
                        {
                            "name": "زبادي يوناني بالعسل والمكسرات",
                            "quantity": "1 كوب زبادي + 1 ملعقة عسل + 20 جرام مكسرات",
                            "alternatives": {
                                "name": "شوفان مطبوخ بالماء مع فواكه مجففة",
                                "quantity": "نصف كوب جاف"
                            }
                        },
                        {
                            "name": "توت",
                            "quantity": "نصف كوب",
                            "alternatives": {
                                "name": "شرائح موز",
                                "quantity": "نصف حبة"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الثالث",
                    "day": "اليوم الثالث",
                    "meal_type": "غداء",
                    "ingredients": [
                        {
                            "name": "أسياخ دجاج مشوية",
                            "quantity": "180 جرام",
                            "alternatives": {
                                "name": "دجاج مفروم بالخضار",
                                "quantity": "180 جرام"
                            }
                        },
                        {
                            "name": "أرز بني",
                            "quantity": "1.5 كوب مطبوخ",
                            "alternatives": {
                                "name": "برغل مطبوخ",
                                "quantity": "1.5 كوب"
                            }
                        },
                        {
                            "name": "سلطة فتوش",
                            "quantity": "1 طبق كبير",
                            "alternatives": {
                                "name": "سلطة كولسلو دايت",
                                "quantity": "1 طبق كبير"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الثالث",
                    "day": "اليوم الثالث",
                    "meal_type": "وجبة خفيفة",
                    "ingredients": [
                        {
                            "name": "فواكه مجففة (كمية قليلة)",
                            "quantity": "30 جرام",
                            "alternatives": {
                                "name": "خيار وجزر",
                                "quantity": "1 كوب"
                            }
                        },
                        {
                            "name": "حمص الشام مسلوق",
                            "quantity": "نصف كوب",
                            "alternatives": {
                                "name": "بذور دوار الشمس",
                                "quantity": "20 جرام"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الثالث",
                    "day": "اليوم الثالث",
                    "meal_type": "عشاء",
                    "ingredients": [
                        {
                            "name": "جبنة قريش",
                            "quantity": "150 جرام",
                            "alternatives": {
                                "name": "بيض مسلوق",
                                "quantity": "2 بيضة"
                            }
                        },
                        {
                            "name": "طماطم",
                            "quantity": "1 حبة متوسطة",
                            "alternatives": {
                                "name": "خس",
                                "quantity": "2 كوب"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الثالث",
                    "day": "اليوم الرابع",
                    "meal_type": "فطور",
                    "ingredients": [
                        {
                            "name": "جبنة فيتا لايت مع خضروات",
                            "quantity": "100 جرام جبنة + 1 كوب خضروات",
                            "alternatives": {
                                "name": "فول مدمس",
                                "quantity": "1 كوب"
                            }
                        },
                        {
                            "name": "زيت بذرة الكتان",
                            "quantity": "1 ملعقة صغيرة",
                            "alternatives": {
                                "name": "زيت زيتون",
                                "quantity": "1 ملعقة صغيرة"
                            }
                        },
                        {
                            "name": "خبز قمح كامل",
                            "quantity": "1 شريحة",
                            "alternatives": {
                                "name": "خبز أسمر",
                                "quantity": "1 شريحة"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الثالث",
                    "day": "اليوم الرابع",
                    "meal_type": "غداء",
                    "ingredients": [
                        {
                            "name": "لحم بقري مفروم قليل الدهن (صينية)",
                            "quantity": "150 جرام",
                            "alternatives": {
                                "name": "كفتة دجاج مشوية",
                                "quantity": "180 جرام"
                            }
                        },
                        {
                            "name": "بطاطا حلوة مشوية",
                            "quantity": "1 حبة متوسطة",
                            "alternatives": {
                                "name": "أرز بني",
                                "quantity": "1.5 كوب مطبوخ"
                            }
                        },
                        {
                            "name": "خضار سوتيه",
                            "quantity": "1 كوب",
                            "alternatives": {
                                "name": "سلطة بنجر وجرجير",
                                "quantity": "1 طبق كبير"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الثالث",
                    "day": "اليوم الرابع",
                    "meal_type": "وجبة خفيفة",
                    "ingredients": [
                        {
                            "name": "مكسرات مشكلة نيئة",
                            "quantity": "30 جرام",
                            "alternatives": {
                                "name": "زبادي لايت",
                                "quantity": "1 كوب"
                            }
                        },
                        {
                            "name": "تفاح",
                            "quantity": "1 حبة متوسطة",
                            "alternatives": {
                                "name": "موز",
                                "quantity": "نصف حبة"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الثالث",
                    "day": "اليوم الرابع",
                    "meal_type": "عشاء",
                    "ingredients": [
                        {
                            "name": "سلطة تونا بالخضروات",
                            "quantity": "1 علبة تونا + 2 كوب خضار",
                            "alternatives": {
                                "name": "سلطة دجاج مشوي",
                                "quantity": "150 جرام دجاج + 2 كوب خضار"
                            }
                        },
                        {
                            "name": "فلفل ألوان",
                            "quantity": "نصف كوب",
                            "alternatives": {
                                "name": "خبز أسمر",
                                "quantity": "1 شريحة"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الثالث",
                    "day": "اليوم الخامس",
                    "meal_type": "فطور",
                    "ingredients": [
                        {
                            "name": "جبنة قريش بالزيتون والخضروات",
                            "quantity": "150 جرام جبنة + 5 حبات زيتون + 1 كوب خضروات",
                            "alternatives": {
                                "name": "شوفان بالحليب قليل الدسم",
                                "quantity": "نصف كوب جاف"
                            }
                        },
                        {
                            "name": "خبز شعير",
                            "quantity": "1 شريحة",
                            "alternatives": {
                                "name": "خبز أسمر",
                                "quantity": "1 شريحة"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الثالث",
                    "day": "اليوم الخامس",
                    "meal_type": "غداء",
                    "ingredients": [
                        {
                            "name": "دجاج مسلوق بالخضار",
                            "quantity": "180 جرام دجاج + 1 كوب خضار",
                            "alternatives": {
                                "name": "سمك بلطي في الفرن بالخضار",
                                "quantity": "200 جرام سمك + 1 كوب خضار"
                            }
                        },
                        {
                            "name": "مكرونة قمح كامل",
                            "quantity": "1.5 كوب مطبوخ",
                            "alternatives": {
                                "name": "أرز بني",
                                "quantity": "1.5 كوب مطبوخ"
                            }
                        },
                        {
                            "name": "شوربة خضار",
                            "quantity": "1 طبق",
                            "alternatives": {
                                "name": "سلطة خضراء كبيرة",
                                "quantity": "1 طبق كبير"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الثالث",
                    "day": "اليوم الخامس",
                    "meal_type": "وجبة خفيفة",
                    "ingredients": [
                        {
                            "name": "توت",
                            "quantity": "1 كوب",
                            "alternatives": {
                                "name": "فراولة",
                                "quantity": "1 كوب"
                            }
                        },
                        {
                            "name": "زبادي يوناني",
                            "quantity": "1 كوب",
                            "alternatives": {
                                "name": "بذور الكتان",
                                "quantity": "1 ملعقة كبيرة"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الثالث",
                    "day": "اليوم الخامس",
                    "meal_type": "عشاء",
                    "ingredients": [
                        {
                            "name": "شوربة بروكلي",
                            "quantity": "2 كوب",
                            "alternatives": {
                                "name": "شوربة عدس",
                                "quantity": "2 كوب"
                            }
                        },
                        {
                            "name": "بقدونس مفروم",
                            "quantity": "2 ملعقة كبيرة",
                            "alternatives": {
                                "name": "خبز أسمر",
                                "quantity": "1 شريحة"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الثالث",
                    "day": "اليوم السادس",
                    "meal_type": "فطور",
                    "ingredients": [
                        {
                            "name": "فول مدمس بالزيت الحار (صحي)",
                            "quantity": "1.5 كوب مطبوخ",
                            "alternatives": {
                                "name": "أومليت بيض بالجبنة",
                                "quantity": "3 بيضات + 50 جرام جبنة"
                            }
                        },
                        {
                            "name": "خبز شوفان",
                            "quantity": "1 رغيف صغير",
                            "alternatives": {
                                "name": "خبز أسمر",
                                "quantity": "1 رغيف صغير"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الثالث",
                    "day": "اليوم السادس",
                    "meal_type": "غداء",
                    "ingredients": [
                        {
                            "name": "سمك مشوي بالليمون",
                            "quantity": "200 جرام",
                            "alternatives": {
                                "name": "صدور دجاج مشوية",
                                "quantity": "180 جرام"
                            }
                        },
                        {
                            "name": "برغل مطبوخ",
                            "quantity": "1.5 كوب",
                            "alternatives": {
                                "name": "أرز بني",
                                "quantity": "1.5 كوب مطبوخ"
                            }
                        },
                        {
                            "name": "خضار سوتيه",
                            "quantity": "1 كوب",
                            "alternatives": {
                                "name": "سلطة ملفوف أبيض وأحمر",
                                "quantity": "1 طبق كبير"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الثالث",
                    "day": "اليوم السادس",
                    "meal_type": "وجبة خفيفة",
                    "ingredients": [
                        {
                            "name": "مكسرات مشكلة نيئة",
                            "quantity": "30 جرام",
                            "alternatives": {
                                "name": "زبادي يوناني",
                                "quantity": "1 كوب"
                            }
                        },
                        {
                            "name": "تفاح",
                            "quantity": "1 حبة",
                            "alternatives": {
                                "name": "موز",
                                "quantity": "نصف حبة"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الثالث",
                    "day": "اليوم السادس",
                    "meal_type": "عشاء",
                    "ingredients": [
                        {
                            "name": "زبادي بالخيار والنعناع",
                            "quantity": "1 كوب زبادي + 1 حبة خيار",
                            "alternatives": {
                                "name": "جبنة قريش",
                                "quantity": "150 جرام"
                            }
                        },
                        {
                            "name": "طماطم شيري",
                            "quantity": "1 كوب",
                            "alternatives": {
                                "name": "خس",
                                "quantity": "2 كوب"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الثالث",
                    "day": "اليوم السابع",
                    "meal_type": "فطور",
                    "ingredients": [
                        {
                            "name": "فول مدمس",
                            "quantity": "1.5 كوب مطبوخ",
                            "alternatives": {
                                "name": "بيض مسلوق",
                                "quantity": "3 بيضات"
                            }
                        },
                        {
                            "name": "طماطم",
                            "quantity": "1 حبة متوسطة",
                            "alternatives": {
                                "name": "خيار",
                                "quantity": "1 حبة"
                            }
                        },
                        {
                            "name": "خبز بلدي أسمر",
                            "quantity": "1 رغيف صغير",
                            "alternatives": {
                                "name": "خبز أسمر",
                                "quantity": "1 رغيف صغير"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الثالث",
                    "day": "اليوم السابع",
                    "meal_type": "غداء",
                    "ingredients": [
                        {
                            "name": "صدور دجاج مشوية",
                            "quantity": "180 جرام",
                            "alternatives": {
                                "name": "لحم بتلو مشوي",
                                "quantity": "150 جرام"
                            }
                        },
                        {
                            "name": "مكرونة قمح كامل",
                            "quantity": "1.5 كوب مطبوخ",
                            "alternatives": {
                                "name": "أرز بني",
                                "quantity": "1.5 كوب مطبوخ"
                            }
                        },
                        {
                            "name": "خضار سوتيه",
                            "quantity": "1 كوب",
                            "alternatives": {
                                "name": "سلطة بلدي",
                                "quantity": "1 طبق كبير"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الثالث",
                    "day": "اليوم السابع",
                    "meal_type": "وجبة خفيفة",
                    "ingredients": [
                        {
                            "name": "كمثرى",
                            "quantity": "1 حبة متوسطة",
                            "alternatives": {
                                "name": "برتقالة",
                                "quantity": "1 حبة"
                            }
                        },
                        {
                            "name": "زبادي لايت",
                            "quantity": "1 كوب",
                            "alternatives": {
                                "name": "لوز نيء",
                                "quantity": "20 جرام"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الثالث",
                    "day": "اليوم السابع",
                    "meal_type": "عشاء",
                    "ingredients": [
                        {
                            "name": "شوربة خضار",
                            "quantity": "2 كوب",
                            "alternatives": {
                                "name": "شوربة عدس",
                                "quantity": "2 كوب"
                            }
                        },
                        {
                            "name": "بصل أخضر",
                            "quantity": "1 عود",
                            "alternatives": {
                                "name": "خبز أسمر",
                                "quantity": "1 شريحة"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الرابع",
                    "day": "اليوم الأول",
                    "meal_type": "فطور",
                    "ingredients": [
                        {
                            "name": "فول مدمس",
                            "quantity": "1.5 كوب مطبوخ",
                            "alternatives": {
                                "name": "بيض مسلوق",
                                "quantity": "3 بيضات"
                            }
                        },
                        {
                            "name": "زيت بذرة الكتان",
                            "quantity": "1 ملعقة كبيرة",
                            "alternatives": {
                                "name": "زيت زيتون",
                                "quantity": "1 ملعقة كبيرة"
                            }
                        },
                        {
                            "name": "خبز بلدي أسمر",
                            "quantity": "1 رغيف صغير",
                            "alternatives": {
                                "name": "خبز شعير",
                                "quantity": "1 رغيف صغير"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الرابع",
                    "day": "اليوم الأول",
                    "meal_type": "غداء",
                    "ingredients": [
                        {
                            "name": "صدور دجاج مشوية",
                            "quantity": "180 جرام",
                            "alternatives": {
                                "name": "سمك فيليه مشوي",
                                "quantity": "200 جرام"
                            }
                        },
                        {
                            "name": "أرز بني مطبوخ",
                            "quantity": "1.5 كوب",
                            "alternatives": {
                                "name": "كينوا مطبوخة",
                                "quantity": "1.5 كوب"
                            }
                        },
                        {
                            "name": "سلطة خضراء مشكلة",
                            "quantity": "1 طبق كبير",
                            "alternatives": {
                                "name": "سلطة كولسلو دايت",
                                "quantity": "1 طبق كبير"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الرابع",
                    "day": "اليوم الأول",
                    "meal_type": "وجبة خفيفة",
                    "ingredients": [
                        {
                            "name": "تفاح",
                            "quantity": "1 حبة متوسطة",
                            "alternatives": {
                                "name": "زبادي يوناني",
                                "quantity": "1 كوب"
                            }
                        },
                        {
                            "name": "عين جمل",
                            "quantity": "30 جرام",
                            "alternatives": {
                                "name": "لوز نيء",
                                "quantity": "30 جرام"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الرابع",
                    "day": "اليوم الأول",
                    "meal_type": "عشاء",
                    "ingredients": [
                        {
                            "name": "جبنة قريش",
                            "quantity": "200 جرام",
                            "alternatives": {
                                "name": "تونا معلبة بالماء ومصفاة",
                                "quantity": "1 علبة صغيرة"
                            }
                        },
                        {
                            "name": "خيار",
                            "quantity": "1 حبة",
                            "alternatives": {
                                "name": "خس",
                                "quantity": "2 كوب"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الرابع",
                    "day": "اليوم الثاني",
                    "meal_type": "فطور",
                    "ingredients": [
                        {
                            "name": "بيض أومليت بالسبانخ",
                            "quantity": "3 بيضات",
                            "alternatives": {
                                "name": "جبنة بيضاء قليلة الدسم",
                                "quantity": "100 جرام"
                            }
                        },
                        {
                            "name": "خبز أسمر",
                            "quantity": "2 شريحة",
                            "alternatives": {
                                "name": "خبز قمح كامل",
                                "quantity": "2 شريحة"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الرابع",
                    "day": "اليوم الثاني",
                    "meal_type": "غداء",
                    "ingredients": [
                        {
                            "name": "لحم بقري قليل الدهن (شرائح)",
                            "quantity": "150 جرام",
                            "alternatives": {
                                "name": "سمك بلطي مشوي",
                                "quantity": "200 جرام"
                            }
                        },
                        {
                            "name": "أرز بني",
                            "quantity": "1.5 كوب مطبوخ",
                            "alternatives": {
                                "name": "مكرونة قمح كامل",
                                "quantity": "1.5 كوب مطبوخ"
                            }
                        },
                        {
                            "name": "خضار سوتيه",
                            "quantity": "1 كوب",
                            "alternatives": {
                                "name": "سلطة خضراء",
                                "quantity": "1 طبق كبير"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الرابع",
                    "day": "اليوم الثاني",
                    "meal_type": "وجبة خفيفة",
                    "ingredients": [
                        {
                            "name": "كمثرى",
                            "quantity": "1 حبة متوسطة",
                            "alternatives": {
                                "name": "برتقالة",
                                "quantity": "1 حبة"
                            }
                        },
                        {
                            "name": "زبادي لايت",
                            "quantity": "1 كوب",
                            "alternatives": {
                                "name": "بذور الشيا",
                                "quantity": "1 ملعقة كبيرة"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الرابع",
                    "day": "اليوم الثاني",
                    "meal_type": "عشاء",
                    "ingredients": [
                        {
                            "name": "شوربة خضار",
                            "quantity": "2 كوب",
                            "alternatives": {
                                "name": "شوربة عدس",
                                "quantity": "2 كوب"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الرابع",
                    "day": "اليوم الثالث",
                    "meal_type": "فطور",
                    "ingredients": [
                        {
                            "name": "فول مدمس بالبيض",
                            "quantity": "1.5 كوب مطبوخ",
                            "alternatives": {
                                "name": "شوفان مطبوخ بالحليب والموز",
                                "quantity": "نصف كوب جاف + نصف موزة"
                            }
                        },
                        {
                            "name": "خبز شوفان",
                            "quantity": "1 رغيف صغير",
                            "alternatives": {
                                "name": "خبز أسمر",
                                "quantity": "1 رغيف صغير"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الرابع",
                    "day": "اليوم الثالث",
                    "meal_type": "غداء",
                    "ingredients": [
                        {
                            "name": "أسياخ دجاج مشوية",
                            "quantity": "180 جرام",
                            "alternatives": {
                                "name": "دجاج مفروم بالخضار",
                                "quantity": "180 جرام"
                            }
                        },
                        {
                            "name": "أرز بني",
                            "quantity": "1.5 كوب مطبوخ",
                            "alternatives": {
                                "name": "برغل مطبوخ",
                                "quantity": "1.5 كوب"
                            }
                        },
                        {
                            "name": "سلطة تبولة",
                            "quantity": "1 طبق كبير",
                            "alternatives": {
                                "name": "سلطة بلدي",
                                "quantity": "1 طبق كبير"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الرابع",
                    "day": "اليوم الثالث",
                    "meal_type": "وجبة خفيفة",
                    "ingredients": [
                        {
                            "name": "خيار وجزر",
                            "quantity": "1 كوب",
                            "alternatives": {
                                "name": "حمص الشام مسلوق",
                                "quantity": "نصف كوب"
                            }
                        },
                        {
                            "name": "زبادي يوناني",
                            "quantity": "1 كوب",
                            "alternatives": {
                                "name": "مكسرات مشكلة",
                                "quantity": "30 جرام"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الرابع",
                    "day": "اليوم الثالث",
                    "meal_type": "عشاء",
                    "ingredients": [
                        {
                            "name": "جبنة قريش",
                            "quantity": "150 جرام",
                            "alternatives": {
                                "name": "بيض مسلوق",
                                "quantity": "2 بيضة"
                            }
                        },
                        {
                            "name": "طماطم",
                            "quantity": "1 حبة متوسطة",
                            "alternatives": {
                                "name": "خس",
                                "quantity": "2 كوب"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الرابع",
                    "day": "اليوم الرابع",
                    "meal_type": "فطور",
                    "ingredients": [
                        {
                            "name": "جبنة فيتا لايت مع خضروات",
                            "quantity": "100 جرام جبنة + 1 كوب خضروات",
                            "alternatives": {
                                "name": "فول مدمس",
                                "quantity": "1 كوب"
                            }
                        },
                        {
                            "name": "زيت بذرة الكتان",
                            "quantity": "1 ملعقة صغيرة",
                            "alternatives": {
                                "name": "زيت زيتون",
                                "quantity": "1 ملعقة صغيرة"
                            }
                        },
                        {
                            "name": "خبز قمح كامل",
                            "quantity": "1 شريحة",
                            "alternatives": {
                                "name": "خبز أسمر",
                                "quantity": "1 شريحة"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الرابع",
                    "day": "اليوم الرابع",
                    "meal_type": "غداء",
                    "ingredients": [
                        {
                            "name": "لحم مفروم بالخضار",
                            "quantity": "150 جرام",
                            "alternatives": {
                                "name": "كفتة دجاج مشوية",
                                "quantity": "180 جرام"
                            }
                        },
                        {
                            "name": "بطاطا حلوة مشوية",
                            "quantity": "1 حبة متوسطة",
                            "alternatives": {
                                "name": "أرز بني",
                                "quantity": "1.5 كوب مطبوخ"
                            }
                        },
                        {
                            "name": "سلطة خضراء",
                            "quantity": "1 طبق كبير",
                            "alternatives": {
                                "name": "سلطة بنجر وجرجير",
                                "quantity": "1 طبق كبير"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الرابع",
                    "day": "اليوم الرابع",
                    "meal_type": "وجبة خفيفة",
                    "ingredients": [
                        {
                            "name": "مكسرات مشكلة نيئة",
                            "quantity": "30 جرام",
                            "alternatives": {
                                "name": "زبادي لايت",
                                "quantity": "1 كوب"
                            }
                        },
                        {
                            "name": "تفاح",
                            "quantity": "1 حبة متوسطة",
                            "alternatives": {
                                "name": "موز",
                                "quantity": "نصف حبة"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الرابع",
                    "day": "اليوم الرابع",
                    "meal_type": "عشاء",
                    "ingredients": [
                        {
                            "name": "سلطة تونا بالخضروات",
                            "quantity": "1 علبة تونا + 2 كوب خضار",
                            "alternatives": {
                                "name": "سلطة دجاج مشوي",
                                "quantity": "150 جرام دجاج + 2 كوب خضار"
                            }
                        },
                        {
                            "name": "فلفل ألوان",
                            "quantity": "نصف كوب",
                            "alternatives": {
                                "name": "خبز أسمر",
                                "quantity": "1 شريحة"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الرابع",
                    "day": "اليوم الخامس",
                    "meal_type": "فطور",
                    "ingredients": [
                        {
                            "name": "جبنة قريش بالزيتون والخضروات",
                            "quantity": "150 جرام جبنة + 5 حبات زيتون + 1 كوب خضروات",
                            "alternatives": {
                                "name": "شوفان بالحليب قليل الدسم",
                                "quantity": "نصف كوب جاف"
                            }
                        },
                        {
                            "name": "خبز شعير",
                            "quantity": "1 شريحة",
                            "alternatives": {
                                "name": "خبز أسمر",
                                "quantity": "1 شريحة"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الرابع",
                    "day": "اليوم الخامس",
                    "meal_type": "غداء",
                    "ingredients": [
                        {
                            "name": "دجاج مسلوق بالخضار",
                            "quantity": "180 جرام دجاج + 1 كوب خضار",
                            "alternatives": {
                                "name": "سمك بلطي في الفرن بالخضار",
                                "quantity": "200 جرام سمك + 1 كوب خضار"
                            }
                        },
                        {
                            "name": "مكرونة قمح كامل",
                            "quantity": "1.5 كوب مطبوخ",
                            "alternatives": {
                                "name": "أرز بني",
                                "quantity": "1.5 كوب مطبوخ"
                            }
                        },
                        {
                            "name": "شوربة خضار",
                            "quantity": "1 طبق",
                            "alternatives": {
                                "name": "سلطة خضراء كبيرة",
                                "quantity": "1 طبق كبير"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الرابع",
                    "day": "اليوم الخامس",
                    "meal_type": "وجبة خفيفة",
                    "ingredients": [
                        {
                            "name": "توت",
                            "quantity": "1 كوب",
                            "alternatives": {
                                "name": "فراولة",
                                "quantity": "1 كوب"
                            }
                        },
                        {
                            "name": "زبادي يوناني",
                            "quantity": "1 كوب",
                            "alternatives": {
                                "name": "بذور الكتان",
                                "quantity": "1 ملعقة كبيرة"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الرابع",
                    "day": "اليوم الخامس",
                    "meal_type": "عشاء",
                    "ingredients": [
                        {
                            "name": "شوربة بروكلي",
                            "quantity": "2 كوب",
                            "alternatives": {
                                "name": "شوربة عدس",
                                "quantity": "2 كوب"
                            }
                        },
                        {
                            "name": "بقدونس مفروم",
                            "quantity": "2 ملعقة كبيرة",
                            "alternatives": {
                                "name": "خبز أسمر",
                                "quantity": "1 شريحة"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الرابع",
                    "day": "اليوم السادس",
                    "meal_type": "فطور",
                    "ingredients": [
                        {
                            "name": "فول مدمس بالزيت الحار (صحي)",
                            "quantity": "1.5 كوب مطبوخ",
                            "alternatives": {
                                "name": "أومليت بيض بالجبنة",
                                "quantity": "3 بيضات + 50 جرام جبنة"
                            }
                        },
                        {
                            "name": "خبز شوفان",
                            "quantity": "1 رغيف صغير",
                            "alternatives": {
                                "name": "خبز أسمر",
                                "quantity": "1 رغيف صغير"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الرابع",
                    "day": "اليوم السادس",
                    "meal_type": "غداء",
                    "ingredients": [
                        {
                            "name": "سمك مشوي بالليمون",
                            "quantity": "200 جرام",
                            "alternatives": {
                                "name": "صدور دجاج مشوية",
                                "quantity": "180 جرام"
                            }
                        },
                        {
                            "name": "برغل مطبوخ",
                            "quantity": "1.5 كوب",
                            "alternatives": {
                                "name": "أرز بني",
                                "quantity": "1.5 كوب مطبوخ"
                            }
                        },
                        {
                            "name": "خضار سوتيه",
                            "quantity": "1 كوب",
                            "alternatives": {
                                "name": "سلطة ملفوف أبيض وأحمر",
                                "quantity": "1 طبق كبير"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الرابع",
                    "day": "اليوم السادس",
                    "meal_type": "وجبة خفيفة",
                    "ingredients": [
                        {
                            "name": "مكسرات مشكلة نيئة",
                            "quantity": "30 جرام",
                            "alternatives": {
                                "name": "زبادي يوناني",
                                "quantity": "1 كوب"
                            }
                        },
                        {
                            "name": "تفاح",
                            "quantity": "1 حبة",
                            "alternatives": {
                                "name": "موز",
                                "quantity": "نصف حبة"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الرابع",
                    "day": "اليوم السادس",
                    "meal_type": "عشاء",
                    "ingredients": [
                        {
                            "name": "زبادي بالخيار والنعناع",
                            "quantity": "1 كوب زبادي + 1 حبة خيار",
                            "alternatives": {
                                "name": "جبنة قريش",
                                "quantity": "150 جرام"
                            }
                        },
                        {
                            "name": "طماطم شيري",
                            "quantity": "1 كوب",
                            "alternatives": {
                                "name": "خس",
                                "quantity": "2 كوب"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الرابع",
                    "day": "اليوم السابع",
                    "meal_type": "فطور",
                    "ingredients": [
                        {
                            "name": "فول مدمس",
                            "quantity": "1.5 كوب مطبوخ",
                            "alternatives": {
                                "name": "بيض مسلوق",
                                "quantity": "3 بيضات"
                            }
                        },
                        {
                            "name": "طماطم",
                            "quantity": "1 حبة متوسطة",
                            "alternatives": {
                                "name": "خيار",
                                "quantity": "1 حبة"
                            }
                        },
                        {
                            "name": "خبز بلدي أسمر",
                            "quantity": "1 رغيف صغير",
                            "alternatives": {
                                "name": "خبز أسمر",
                                "quantity": "1 رغيف صغير"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الرابع",
                    "day": "اليوم السابع",
                    "meal_type": "غداء",
                    "ingredients": [
                        {
                            "name": "صدور دجاج مشوية",
                            "quantity": "180 جرام",
                            "alternatives": {
                                "name": "لحم بتلو مشوي",
                                "quantity": "150 جرام"
                            }
                        },
                        {
                            "name": "مكرونة قمح كامل",
                            "quantity": "1.5 كوب مطبوخ",
                            "alternatives": {
                                "name": "أرز بني",
                                "quantity": "1.5 كوب مطبوخ"
                            }
                        },
                        {
                            "name": "خضار سوتيه",
                            "quantity": "1 كوب",
                            "alternatives": {
                                "name": "سلطة بلدي",
                                "quantity": "1 طبق كبير"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الرابع",
                    "day": "اليوم السابع",
                    "meal_type": "وجبة خفيفة",
                    "ingredients": [
                        {
                            "name": "كمثرى",
                            "quantity": "1 حبة متوسطة",
                            "alternatives": {
                                "name": "برتقالة",
                                "quantity": "1 حبة"
                            }
                        },
                        {
                            "name": "زبادي لايت",
                            "quantity": "1 كوب",
                            "alternatives": {
                                "name": "لوز نيء",
                                "quantity": "20 جرام"
                            }
                        }
                    ]
                },
                {
                    "week": "الأسبوع الرابع",
                    "day": "اليوم السابع",
                    "meal_type": "عشاء",
                    "ingredients": [
                        {
                            "name": "شوربة خضار",
                            "quantity": "2 كوب",
                            "alternatives": {
                                "name": "شوربة عدس",
                                "quantity": "2 كوب"
                            }
                        },
                        {
                            "name": "بصل أخضر",
                            "quantity": "1 عود",
                            "alternatives": {
                                "name": "خبز أسمر",
                                "quantity": "1 شريحة"
                            }
                        }
                    ]
                }
            ]
        }
        
x=convert_flat_to_nested(plan)
with open("x.json", "w", encoding="utf-8") as f:
    json.dump(x, f, ensure_ascii=False, indent=4)

