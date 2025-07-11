"""
DSM-5 TR Hierarchical Symptom Structure for Clinical Assessment
"""

DSM5_HIERARCHY = {
    "Mood Disorders": {
        "Major Depressive Disorder": {
            "core_symptoms": [
                {"name": "Depressed mood most of the day, nearly every day", "code": "A1", "required": True},
                {"name": "Markedly diminished interest or pleasure in activities (anhedonia)", "code": "A2", "required": True},
            ],
            "additional_symptoms": [
                {"name": "Significant weight loss or weight gain, or appetite changes", "code": "A3"},
                {"name": "Insomnia or hypersomnia nearly every day", "code": "A4"},
                {"name": "Psychomotor agitation or retardation nearly every day", "code": "A5"},
                {"name": "Fatigue or loss of energy nearly every day", "code": "A6"},
                {"name": "Feelings of worthlessness or excessive/inappropriate guilt", "code": "A7"},
                {"name": "Diminished ability to think or concentrate, indecisiveness", "code": "A8"},
                {"name": "Recurrent thoughts of death, suicidal ideation, or suicide attempt", "code": "A9"},
            ],
            "severity_specifiers": ["Mild", "Moderate", "Severe"],
            "episode_specifiers": ["Single Episode", "Recurrent"],
            "features": ["With anxious distress", "With melancholic features", "With atypical features", "With psychotic features"]
        },
        "Persistent Depressive Disorder (Dysthymia)": {
            "core_symptoms": [
                {"name": "Depressed mood for most of the day, more days than not, for at least 2 years", "code": "B1", "required": True}
            ],
            "associated_symptoms": [
                {"name": "Poor appetite or overeating", "code": "B2"},
                {"name": "Insomnia or hypersomnia", "code": "B3"},
                {"name": "Low energy or fatigue", "code": "B4"},
                {"name": "Low self-esteem", "code": "B5"},
                {"name": "Poor concentration or difficulty making decisions", "code": "B6"},
                {"name": "Feelings of hopelessness", "code": "B7"},
            ]
        },
        "Bipolar I Disorder": {
            "manic_episode": [
                {"name": "Abnormally elevated, expansive, or irritable mood and energy", "code": "C1", "required": True},
                {"name": "Persistently increased activity or energy", "code": "C2", "required": True},
            ],
            "manic_symptoms": [
                {"name": "Inflated self-esteem or grandiosity", "code": "C3"},
                {"name": "Decreased need for sleep (feels rested after 3 hours)", "code": "C4"},
                {"name": "More talkative than usual or pressure to keep talking", "code": "C5"},
                {"name": "Flight of ideas or racing thoughts", "code": "C6"},
                {"name": "Distractibility (attention easily drawn to irrelevant stimuli)", "code": "C7"},
                {"name": "Increase in goal-directed activity or psychomotor agitation", "code": "C8"},
                {"name": "Excessive involvement in risky activities", "code": "C9"},
            ]
        },
        "Bipolar II Disorder": {
            "hypomanic_episode": [
                {"name": "Elevated, expansive, or irritable mood and energy for at least 4 days", "code": "D1", "required": True}
            ],
            "depressive_episode": [
                {"name": "At least one major depressive episode", "code": "D2", "required": True}
            ]
        }
    },
    "Anxiety Disorders": {
        "Generalized Anxiety Disorder": {
            "core_symptoms": [
                {"name": "Excessive anxiety and worry about various events/activities", "code": "E1", "required": True},
                {"name": "Difficult to control the worry", "code": "E2", "required": True},
            ],
            "associated_symptoms": [
                {"name": "Restlessness or feeling keyed up or on edge", "code": "E3"},
                {"name": "Being easily fatigued", "code": "E4"},
                {"name": "Difficulty concentrating or mind going blank", "code": "E5"},
                {"name": "Irritability", "code": "E6"},
                {"name": "Muscle tension", "code": "E7"},
                {"name": "Sleep disturbance (difficulty falling/staying asleep)", "code": "E8"},
            ]
        },
        "Panic Disorder": {
            "panic_attacks": [
                {"name": "Palpitations, pounding heart, or accelerated heart rate", "code": "F1"},
                {"name": "Sweating", "code": "F2"},
                {"name": "Trembling or shaking", "code": "F3"},
                {"name": "Sensations of shortness of breath or smothering", "code": "F4"},
                {"name": "Feelings of choking", "code": "F5"},
                {"name": "Chest pain or discomfort", "code": "F6"},
                {"name": "Nausea or abdominal distress", "code": "F7"},
                {"name": "Feeling dizzy, unsteady, light-headed, or faint", "code": "F8"},
                {"name": "Chills or heat sensations", "code": "F9"},
                {"name": "Paresthesias (numbness or tingling sensations)", "code": "F10"},
                {"name": "Derealization or depersonalization", "code": "F11"},
                {"name": "Fear of losing control or going crazy", "code": "F12"},
                {"name": "Fear of dying", "code": "F13"},
            ],
            "additional_criteria": [
                {"name": "Recurrent unexpected panic attacks", "code": "F14", "required": True},
                {"name": "Persistent concern about having additional attacks", "code": "F15"},
                {"name": "Significant maladaptive change in behavior related to attacks", "code": "F16"},
            ]
        },
        "Social Anxiety Disorder": {
            "core_symptoms": [
                {"name": "Marked fear/anxiety about social situations with possible scrutiny", "code": "G1", "required": True},
                {"name": "Fear of acting in ways that will be negatively evaluated", "code": "G2", "required": True},
            ],
            "behavioral_symptoms": [
                {"name": "Social situations almost always provoke fear or anxiety", "code": "G3"},
                {"name": "Social situations are avoided or endured with intense fear", "code": "G4"},
                {"name": "Fear/anxiety is out of proportion to actual threat", "code": "G5"},
            ]
        },
        "Specific Phobia": {
            "core_symptoms": [
                {"name": "Marked fear or anxiety about a specific object or situation", "code": "H1", "required": True},
                {"name": "Phobic object/situation almost always provokes immediate fear", "code": "H2", "required": True},
                {"name": "Phobic object/situation is actively avoided", "code": "H3", "required": True},
            ],
            "specifiers": ["Animal", "Natural environment", "Blood-injection-injury", "Situational", "Other"]
        }
    },
    "Trauma and Stressor-Related Disorders": {
        "Posttraumatic Stress Disorder": {
            "criterion_a": [
                {"name": "Exposure to actual or threatened death, serious injury, or sexual violence", "code": "I1", "required": True}
            ],
            "criterion_b_intrusion": [
                {"name": "Recurrent, involuntary, and intrusive distressing memories", "code": "I2"},
                {"name": "Recurrent distressing dreams related to the traumatic event", "code": "I3"},
                {"name": "Dissociative reactions (flashbacks)", "code": "I4"},
                {"name": "Intense or prolonged psychological distress at trauma cues", "code": "I5"},
                {"name": "Marked physiological reactions to trauma cues", "code": "I6"},
            ],
            "criterion_c_avoidance": [
                {"name": "Avoidance of trauma-related thoughts, feelings, or memories", "code": "I7"},
                {"name": "Avoidance of external reminders of the trauma", "code": "I8"},
            ],
            "criterion_d_cognition_mood": [
                {"name": "Inability to remember important aspect of the trauma", "code": "I9"},
                {"name": "Persistent negative beliefs about oneself, others, or world", "code": "I10"},
                {"name": "Persistent distorted cognitions about cause/consequences of trauma", "code": "I11"},
                {"name": "Persistent negative emotional state", "code": "I12"},
                {"name": "Markedly diminished interest or participation in activities", "code": "I13"},
                {"name": "Feelings of detachment or estrangement from others", "code": "I14"},
                {"name": "Persistent inability to experience positive emotions", "code": "I15"},
            ],
            "criterion_e_arousal": [
                {"name": "Irritable behavior and angry outbursts", "code": "I16"},
                {"name": "Reckless or self-destructive behavior", "code": "I17"},
                {"name": "Hypervigilance", "code": "I18"},
                {"name": "Exaggerated startle response", "code": "I19"},
                {"name": "Problems with concentration", "code": "I20"},
                {"name": "Sleep disturbance", "code": "I21"},
            ]
        },
        "Acute Stress Disorder": {
            "core_symptoms": [
                {"name": "Exposure to actual or threatened death, serious injury, or sexual violence", "code": "J1", "required": True},
                {"name": "Symptoms present for 3 days to 1 month after trauma", "code": "J2", "required": True},
            ],
            "symptom_clusters": [
                {"name": "Intrusion symptoms (memories, dreams, flashbacks)", "code": "J3"},
                {"name": "Negative mood", "code": "J4"},
                {"name": "Dissociative symptoms", "code": "J5"},
                {"name": "Avoidance symptoms", "code": "J6"},
                {"name": "Arousal symptoms", "code": "J7"},
            ]
        }
    },
    "Obsessive-Compulsive and Related Disorders": {
        "Obsessive-Compulsive Disorder": {
            "obsessions": [
                {"name": "Recurrent and persistent thoughts, urges, or images", "code": "K1"},
                {"name": "Thoughts/urges/images are intrusive and unwanted", "code": "K2"},
                {"name": "Attempts to ignore or suppress thoughts or neutralize with actions", "code": "K3"},
            ],
            "compulsions": [
                {"name": "Repetitive behaviors (hand washing, ordering, checking)", "code": "K4"},
                {"name": "Mental acts (praying, counting, repeating words)", "code": "K5"},
                {"name": "Behaviors/acts aimed at preventing or reducing anxiety", "code": "K6"},
                {"name": "Behaviors/acts are not connected realistically to threat", "code": "K7"},
            ]
        }
    },
    "Substance-Related and Addictive Disorders": {
        "Alcohol Use Disorder": {
            "core_criteria": [
                {"name": "Alcohol taken in larger amounts or longer period than intended", "code": "L1"},
                {"name": "Persistent desire or unsuccessful efforts to cut down", "code": "L2"},
                {"name": "Great deal of time spent obtaining, using, or recovering from alcohol", "code": "L3"},
                {"name": "Craving or strong desire to use alcohol", "code": "L4"},
                {"name": "Recurrent use resulting in failure to fulfill role obligations", "code": "L5"},
                {"name": "Continued use despite social or interpersonal problems", "code": "L6"},
                {"name": "Important activities given up or reduced because of alcohol use", "code": "L7"},
                {"name": "Recurrent use in physically hazardous situations", "code": "L8"},
                {"name": "Continued use despite physical or psychological problems", "code": "L9"},
                {"name": "Tolerance (need increased amounts or diminished effect)", "code": "L10"},
                {"name": "Withdrawal (characteristic syndrome or alcohol to relieve withdrawal)", "code": "L11"},
            ],
            "severity_levels": {
                "mild": "2-3 symptoms",
                "moderate": "4-5 symptoms", 
                "severe": "6+ symptoms"
            }
        }
    },
    "Schizophrenia Spectrum and Other Psychotic Disorders": {
        "Schizophrenia": {
            "positive_symptoms": [
                {"name": "Delusions", "code": "M1"},
                {"name": "Hallucinations", "code": "M2"},
                {"name": "Disorganized thinking (speech)", "code": "M3"},
                {"name": "Grossly disorganized or abnormal motor behavior", "code": "M4"},
            ],
            "negative_symptoms": [
                {"name": "Diminished emotional expression", "code": "M5"},
                {"name": "Avolition (decreased motivated self-initiated purposeful activities)", "code": "M6"},
            ]
        },
        "Brief Psychotic Disorder": {
            "core_symptoms": [
                {"name": "Sudden onset of psychotic symptoms", "code": "N1", "required": True},
                {"name": "Duration of at least 1 day but less than 1 month", "code": "N2", "required": True},
                {"name": "Eventual return to normal level of functioning", "code": "N3", "required": True},
            ]
        }
    },
    "Attention-Deficit/Hyperactivity Disorder": {
        "ADHD": {
            "inattention_symptoms": [
                {"name": "Fails to give close attention to details or makes careless mistakes", "code": "O1"},
                {"name": "Has difficulty sustaining attention in tasks or play", "code": "O2"},
                {"name": "Does not seem to listen when spoken to directly", "code": "O3"},
                {"name": "Does not follow through on instructions and fails to finish work", "code": "O4"},
                {"name": "Has difficulty organizing tasks and activities", "code": "O5"},
                {"name": "Avoids tasks that require sustained mental effort", "code": "O6"},
                {"name": "Loses things necessary for tasks or activities", "code": "O7"},
                {"name": "Is easily distracted by extraneous stimuli", "code": "O8"},
                {"name": "Is forgetful in daily activities", "code": "O9"},
            ],
            "hyperactivity_impulsivity": [
                {"name": "Fidgets with hands/feet or squirms in seat", "code": "O10"},
                {"name": "Leaves seat when remaining seated is expected", "code": "O11"},
                {"name": "Runs about or climbs inappropriately", "code": "O12"},
                {"name": "Unable to play or engage in leisure activities quietly", "code": "O13"},
                {"name": "Is on the go, acting as if driven by a motor", "code": "O14"},
                {"name": "Talks excessively", "code": "O15"},
                {"name": "Blurts out answers before questions completed", "code": "O16"},
                {"name": "Has difficulty waiting turn", "code": "O17"},
                {"name": "Interrupts or intrudes on others", "code": "O18"},
            ],
            "subtypes": ["Combined presentation", "Predominantly inattentive", "Predominantly hyperactive-impulsive"]
        }
    }
}

# Clinical scales and assessment tools
CLINICAL_SCALES = {
    "Depression": {
        "PHQ-9": {
            "name": "Patient Health Questionnaire-9",
            "range": "0-27",
            "interpretation": {
                "0-4": "Minimal depression",
                "5-9": "Mild depression", 
                "10-14": "Moderate depression",
                "15-19": "Moderately severe depression",
                "20-27": "Severe depression"
            }
        },
        "Beck Depression Inventory": {
            "name": "Beck Depression Inventory-II",
            "range": "0-63",
            "interpretation": {
                "0-13": "Minimal depression",
                "14-19": "Mild depression",
                "20-28": "Moderate depression", 
                "29-63": "Severe depression"
            }
        }
    },
    "Anxiety": {
        "GAD-7": {
            "name": "Generalized Anxiety Disorder 7-item",
            "range": "0-21",
            "interpretation": {
                "0-4": "Minimal anxiety",
                "5-9": "Mild anxiety",
                "10-14": "Moderate anxiety",
                "15-21": "Severe anxiety"
            }
        },
        "Beck Anxiety Inventory": {
            "name": "Beck Anxiety Inventory",
            "range": "0-63",
            "interpretation": {
                "0-7": "Minimal anxiety",
                "8-15": "Mild anxiety",
                "16-25": "Moderate anxiety",
                "26-63": "Severe anxiety"
            }
        }
    },
    "PTSD": {
        "PCL-5": {
            "name": "PTSD Checklist for DSM-5",
            "range": "0-80",
            "interpretation": {
                "0-32": "Below threshold",
                "33-80": "Probable PTSD (requires clinical assessment)"
            }
        }
    },
    "Mania": {
        "YMRS": {
            "name": "Young Mania Rating Scale",
            "range": "0-60",
            "interpretation": {
                "0-12": "Normal/remission",
                "13-19": "Mild mania",
                "20-25": "Moderate mania",
                "26-60": "Severe mania"
            }
        }
    },
    "Psychosis": {
        "PANSS": {
            "name": "Positive and Negative Syndrome Scale",
            "subscales": {
                "positive": "7-49",
                "negative": "7-49", 
                "general": "16-112"
            }
        }
    }
}

def get_disorder_by_category(category):
    """Get all disorders in a specific category"""
    return DSM5_HIERARCHY.get(category, {})

def get_symptoms_by_disorder(category, disorder):
    """Get all symptoms for a specific disorder"""
    return DSM5_HIERARCHY.get(category, {}).get(disorder, {})

def get_required_symptoms(category, disorder):
    """Get required symptoms for diagnosis"""
    disorder_data = get_symptoms_by_disorder(category, disorder)
    required_symptoms = []
    
    for symptom_group, symptoms in disorder_data.items():
        if isinstance(symptoms, list):
            required_symptoms.extend([s for s in symptoms if s.get('required', False)])
    
    return required_symptoms