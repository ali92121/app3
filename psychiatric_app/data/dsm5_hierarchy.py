"""
DSM-5 TR Hierarchical Structure for Psychiatric Symptom Assessment.
Comprehensive mapping of psychiatric disorders and their symptoms according to DSM-5 TR criteria.
"""

DSM5_HIERARCHY = {
    "Mood Disorders": {
        "Major Depressive Disorder": {
            "core_symptoms": [
                {"name": "Depressed mood most of the day, nearly every day", "code": "A1", "required": True, "criterion": "A"},
                {"name": "Markedly diminished interest or pleasure in activities (anhedonia)", "code": "A2", "required": True, "criterion": "A"},
            ],
            "additional_symptoms": [
                {"name": "Significant weight loss or weight gain (>5% body weight in a month)", "code": "A3", "criterion": "A"},
                {"name": "Insomnia or hypersomnia nearly every day", "code": "A4", "criterion": "A"},
                {"name": "Psychomotor agitation or retardation nearly every day", "code": "A5", "criterion": "A"},
                {"name": "Fatigue or loss of energy nearly every day", "code": "A6", "criterion": "A"},
                {"name": "Feelings of worthlessness or excessive/inappropriate guilt", "code": "A7", "criterion": "A"},
                {"name": "Diminished ability to think or concentrate, or indecisiveness", "code": "A8", "criterion": "A"},
                {"name": "Recurrent thoughts of death or recurrent suicidal ideation", "code": "A9", "criterion": "A"},
            ],
            "severity_specifiers": ["Mild", "Moderate", "Severe"],
            "episode_specifiers": ["Single Episode", "Recurrent"],
            "features": [
                "With anxious distress",
                "With melancholic features", 
                "With atypical features",
                "With mood-congruent psychotic features",
                "With mood-incongruent psychotic features",
                "With catatonia",
                "With peripartum onset",
                "With seasonal pattern"
            ],
            "duration_requirement": "2 weeks",
            "functional_impairment_required": True
        },
        "Bipolar I Disorder": {
            "manic_episode_core": [
                {"name": "Elevated, expansive, or irritable mood", "code": "B1", "required": True, "criterion": "A"},
                {"name": "Abnormally and persistently increased goal-directed activity or energy", "code": "B2", "required": True, "criterion": "A"},
            ],
            "manic_symptoms": [
                {"name": "Inflated self-esteem or grandiosity", "code": "B3", "criterion": "B"},
                {"name": "Decreased need for sleep (feels rested after only 3 hours)", "code": "B4", "criterion": "B"},
                {"name": "More talkative than usual or pressure to keep talking", "code": "B5", "criterion": "B"},
                {"name": "Flight of ideas or subjective experience of racing thoughts", "code": "B6", "criterion": "B"},
                {"name": "Distractibility as reported or observed", "code": "B7", "criterion": "B"},
                {"name": "Increase in goal-directed activity or psychomotor agitation", "code": "B8", "criterion": "B"},
                {"name": "Excessive involvement in risky activities", "code": "B9", "criterion": "B"},
            ],
            "duration_requirement": "1 week (or any duration if hospitalization is necessary)",
            "functional_impairment_required": True,
            "severity_specifiers": ["Mild", "Moderate", "Severe"],
            "features": [
                "With anxious distress",
                "With rapid cycling",
                "With mood-congruent psychotic features",
                "With mood-incongruent psychotic features",
                "With catatonia"
            ]
        },
        "Bipolar II Disorder": {
            "hypomanic_episode": [
                {"name": "Elevated, expansive, or irritable mood", "code": "C1", "criterion": "A"},
                {"name": "Abnormally and persistently increased activity or energy", "code": "C2", "criterion": "A"},
            ],
            "hypomanic_symptoms": [
                {"name": "Inflated self-esteem or grandiosity", "code": "C3", "criterion": "B"},
                {"name": "Decreased need for sleep", "code": "C4", "criterion": "B"},
                {"name": "More talkative than usual", "code": "C5", "criterion": "B"},
                {"name": "Flight of ideas or racing thoughts", "code": "C6", "criterion": "B"},
                {"name": "Distractibility", "code": "C7", "criterion": "B"},
                {"name": "Increase in goal-directed activity", "code": "C8", "criterion": "B"},
                {"name": "Excessive involvement in risky activities", "code": "C9", "criterion": "B"},
            ],
            "major_depressive_episode": [
                {"name": "History of at least one major depressive episode", "code": "C10", "required": True}
            ],
            "duration_requirement": "4 consecutive days",
            "functional_impairment_required": False
        },
        "Persistent Depressive Disorder (Dysthymia)": {
            "core_symptoms": [
                {"name": "Depressed mood for most of the day, more days than not", "code": "D1", "required": True},
            ],
            "associated_symptoms": [
                {"name": "Poor appetite or overeating", "code": "D2"},
                {"name": "Insomnia or hypersomnia", "code": "D3"},
                {"name": "Low energy or fatigue", "code": "D4"},
                {"name": "Low self-esteem", "code": "D5"},
                {"name": "Poor concentration or difficulty making decisions", "code": "D6"},
                {"name": "Feelings of hopelessness", "code": "D7"},
            ],
            "duration_requirement": "2 years (1 year for children/adolescents)",
            "severity_specifiers": ["Mild", "Moderate", "Severe"]
        }
    },
    "Anxiety Disorders": {
        "Generalized Anxiety Disorder": {
            "core_symptoms": [
                {"name": "Excessive anxiety and worry about various events/activities", "code": "E1", "required": True, "criterion": "A"},
                {"name": "Difficult to control the worry", "code": "E2", "required": True, "criterion": "B"},
            ],
            "associated_symptoms": [
                {"name": "Restlessness or feeling keyed up or on edge", "code": "E3", "criterion": "C"},
                {"name": "Being easily fatigued", "code": "E4", "criterion": "C"},
                {"name": "Difficulty concentrating or mind going blank", "code": "E5", "criterion": "C"},
                {"name": "Irritability", "code": "E6", "criterion": "C"},
                {"name": "Muscle tension", "code": "E7", "criterion": "C"},
                {"name": "Sleep disturbance", "code": "E8", "criterion": "C"},
            ],
            "duration_requirement": "6 months",
            "functional_impairment_required": True
        },
        "Panic Disorder": {
            "panic_attack_symptoms": [
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
                {"name": "Persistent concern about additional panic attacks", "code": "F15"},
                {"name": "Significant maladaptive change in behavior related to attacks", "code": "F16"},
            ],
            "duration_requirement": "1 month",
            "panic_attack_duration": "Peak within minutes"
        },
        "Social Anxiety Disorder": {
            "core_symptoms": [
                {"name": "Marked fear/anxiety about social situations where scrutinized by others", "code": "G1", "required": True},
                {"name": "Fear of acting in ways that will be negatively evaluated", "code": "G2", "required": True},
            ],
            "additional_criteria": [
                {"name": "Social situations almost always provoke fear or anxiety", "code": "G3"},
                {"name": "Social situations are avoided or endured with intense fear/anxiety", "code": "G4"},
                {"name": "Fear/anxiety is out of proportion to actual threat", "code": "G5"},
                {"name": "Fear/anxiety/avoidance is persistent", "code": "G6"},
            ],
            "duration_requirement": "6 months",
            "functional_impairment_required": True,
            "specifiers": ["Performance only"]
        },
        "Specific Phobia": {
            "core_symptoms": [
                {"name": "Marked fear or anxiety about a specific object or situation", "code": "H1", "required": True},
                {"name": "Phobic object/situation almost always provokes fear/anxiety", "code": "H2"},
                {"name": "Phobic object/situation is actively avoided", "code": "H3"},
                {"name": "Fear/anxiety is out of proportion to actual danger", "code": "H4"},
                {"name": "Fear/anxiety/avoidance is persistent", "code": "H5"},
            ],
            "duration_requirement": "6 months",
            "phobia_types": [
                "Animal", "Natural environment", "Blood-injection-injury", 
                "Situational", "Other"
            ]
        }
    },
    "Trauma and Stressor-Related Disorders": {
        "Posttraumatic Stress Disorder (PTSD)": {
            "criterion_a": [
                {"name": "Exposure to actual or threatened death, serious injury, or sexual violence", "code": "I1", "required": True, "criterion": "A"}
            ],
            "criterion_b_intrusion": [
                {"name": "Recurrent, involuntary, and intrusive distressing memories", "code": "I2", "criterion": "B"},
                {"name": "Recurrent distressing dreams related to the traumatic event", "code": "I3", "criterion": "B"},
                {"name": "Dissociative reactions (flashbacks)", "code": "I4", "criterion": "B"},
                {"name": "Intense or prolonged psychological distress to trauma cues", "code": "I5", "criterion": "B"},
                {"name": "Marked physiological reactions to trauma reminders", "code": "I6", "criterion": "B"},
            ],
            "criterion_c_avoidance": [
                {"name": "Avoidance of or efforts to avoid distressing trauma-related thoughts/feelings", "code": "I7", "criterion": "C"},
                {"name": "Avoidance of or efforts to avoid external trauma reminders", "code": "I8", "criterion": "C"},
            ],
            "criterion_d_cognition_mood": [
                {"name": "Inability to remember important aspect of traumatic event", "code": "I9", "criterion": "D"},
                {"name": "Persistent negative beliefs about oneself, others, or the world", "code": "I10", "criterion": "D"},
                {"name": "Persistent distorted cognitions about cause/consequences of trauma", "code": "I11", "criterion": "D"},
                {"name": "Persistent negative emotional state", "code": "I12", "criterion": "D"},
                {"name": "Markedly diminished interest/participation in significant activities", "code": "I13", "criterion": "D"},
                {"name": "Feelings of detachment or estrangement from others", "code": "I14", "criterion": "D"},
                {"name": "Persistent inability to experience positive emotions", "code": "I15", "criterion": "D"},
            ],
            "criterion_e_arousal": [
                {"name": "Irritable behavior and angry outbursts", "code": "I16", "criterion": "E"},
                {"name": "Reckless or self-destructive behavior", "code": "I17", "criterion": "E"},
                {"name": "Hypervigilance", "code": "I18", "criterion": "E"},
                {"name": "Exaggerated startle response", "code": "I19", "criterion": "E"},
                {"name": "Problems with concentration", "code": "I20", "criterion": "E"},
                {"name": "Sleep disturbance", "code": "I21", "criterion": "E"},
            ],
            "duration_requirement": "1 month",
            "functional_impairment_required": True,
            "specifiers": [
                "With dissociative symptoms",
                "With delayed expression"
            ]
        },
        "Acute Stress Disorder": {
            "trauma_exposure": [
                {"name": "Exposure to actual or threatened death, serious injury, or sexual violence", "code": "J1", "required": True}
            ],
            "stress_symptoms": [
                {"name": "Recurrent, involuntary, and intrusive distressing memories", "code": "J2"},
                {"name": "Recurrent distressing dreams", "code": "J3"},
                {"name": "Dissociative reactions (flashbacks)", "code": "J4"},
                {"name": "Intense or prolonged psychological distress", "code": "J5"},
                {"name": "Marked physiological reactions", "code": "J6"},
                {"name": "Persistent inability to experience positive emotions", "code": "J7"},
                {"name": "Altered sense of reality of surroundings or oneself", "code": "J8"},
                {"name": "Inability to remember important aspect of traumatic event", "code": "J9"},
                {"name": "Efforts to avoid distressing trauma-related thoughts/feelings", "code": "J10"},
                {"name": "Efforts to avoid external trauma reminders", "code": "J11"},
                {"name": "Sleep disturbance", "code": "J12"},
                {"name": "Irritable behavior and angry outbursts", "code": "J13"},
                {"name": "Hypervigilance", "code": "J14"},
                {"name": "Problems with concentration", "code": "J15"},
                {"name": "Exaggerated startle response", "code": "J16"},
            ],
            "duration_requirement": "3 days to 1 month",
            "functional_impairment_required": True
        }
    },
    "Attention-Deficit/Hyperactivity Disorder": {
        "ADHD Combined Presentation": {
            "inattention_symptoms": [
                {"name": "Fails to give close attention to details or makes careless mistakes", "code": "K1", "criterion": "A1"},
                {"name": "Has difficulty sustaining attention in tasks or play", "code": "K2", "criterion": "A1"},
                {"name": "Does not seem to listen when spoken to directly", "code": "K3", "criterion": "A1"},
                {"name": "Does not follow through on instructions", "code": "K4", "criterion": "A1"},
                {"name": "Has difficulty organizing tasks and activities", "code": "K5", "criterion": "A1"},
                {"name": "Avoids tasks that require sustained mental effort", "code": "K6", "criterion": "A1"},
                {"name": "Loses things necessary for tasks or activities", "code": "K7", "criterion": "A1"},
                {"name": "Easily distracted by extraneous stimuli", "code": "K8", "criterion": "A1"},
                {"name": "Forgetful in daily activities", "code": "K9", "criterion": "A1"},
            ],
            "hyperactivity_impulsivity_symptoms": [
                {"name": "Fidgets with or taps hands or feet or squirms in seat", "code": "K10", "criterion": "A2"},
                {"name": "Leaves seat in situations when remaining seated is expected", "code": "K11", "criterion": "A2"},
                {"name": "Runs about or climbs in inappropriate situations", "code": "K12", "criterion": "A2"},
                {"name": "Unable to play or engage in leisure activities quietly", "code": "K13", "criterion": "A2"},
                {"name": "Is 'on the go,' acting as if 'driven by a motor'", "code": "K14", "criterion": "A2"},
                {"name": "Talks excessively", "code": "K15", "criterion": "A2"},
                {"name": "Blurts out answers before questions have been completed", "code": "K16", "criterion": "A2"},
                {"name": "Has difficulty waiting his or her turn", "code": "K17", "criterion": "A2"},
                {"name": "Interrupts or intrudes on others", "code": "K18", "criterion": "A2"},
            ],
            "onset_requirement": "Before age 12",
            "duration_requirement": "6 months",
            "setting_requirement": "Two or more settings",
            "functional_impairment_required": True,
            "presentations": [
                "Combined presentation",
                "Predominantly inattentive presentation", 
                "Predominantly hyperactive/impulsive presentation"
            ]
        }
    },
    "Substance-Related and Addictive Disorders": {
        "Alcohol Use Disorder": {
            "use_disorder_criteria": [
                {"name": "Alcohol taken in larger amounts or longer than intended", "code": "L1", "criterion": "A"},
                {"name": "Persistent desire or unsuccessful efforts to cut down/control use", "code": "L2", "criterion": "A"},
                {"name": "Great deal of time spent obtaining, using, or recovering from alcohol", "code": "L3", "criterion": "A"},
                {"name": "Craving or strong desire to use alcohol", "code": "L4", "criterion": "A"},
                {"name": "Recurrent use resulting in failure to fulfill role obligations", "code": "L5", "criterion": "A"},
                {"name": "Continued use despite persistent social/interpersonal problems", "code": "L6", "criterion": "A"},
                {"name": "Important activities given up or reduced because of alcohol use", "code": "L7", "criterion": "A"},
                {"name": "Recurrent use in physically hazardous situations", "code": "L8", "criterion": "A"},
                {"name": "Continued use despite knowledge of physical/psychological problems", "code": "L9", "criterion": "A"},
                {"name": "Tolerance", "code": "L10", "criterion": "A"},
                {"name": "Withdrawal", "code": "L11", "criterion": "A"},
            ],
            "severity_levels": {
                "Mild": "2-3 symptoms",
                "Moderate": "4-5 symptoms", 
                "Severe": "6 or more symptoms"
            },
            "duration_requirement": "12 months",
            "specifiers": [
                "In early remission",
                "In sustained remission", 
                "In a controlled environment"
            ]
        },
        "Cannabis Use Disorder": {
            "use_disorder_criteria": [
                {"name": "Cannabis taken in larger amounts or longer than intended", "code": "M1"},
                {"name": "Persistent desire or unsuccessful efforts to cut down/control use", "code": "M2"},
                {"name": "Great deal of time spent in cannabis-related activities", "code": "M3"},
                {"name": "Craving or strong desire to use cannabis", "code": "M4"},
                {"name": "Recurrent use resulting in failure to fulfill obligations", "code": "M5"},
                {"name": "Continued use despite social/interpersonal problems", "code": "M6"},
                {"name": "Important activities given up because of cannabis use", "code": "M7"},
                {"name": "Recurrent use in hazardous situations", "code": "M8"},
                {"name": "Continued use despite physical/psychological problems", "code": "M9"},
                {"name": "Tolerance", "code": "M10"},
                {"name": "Withdrawal", "code": "M11"},
            ],
            "withdrawal_symptoms": [
                {"name": "Irritability, anger, or aggression", "code": "M12"},
                {"name": "Nervousness or anxiety", "code": "M13"},
                {"name": "Sleep difficulty", "code": "M14"},
                {"name": "Decreased appetite or weight loss", "code": "M15"},
                {"name": "Restlessness", "code": "M16"},
                {"name": "Depressed mood", "code": "M17"},
                {"name": "Physical symptoms causing significant discomfort", "code": "M18"},
            ]
        }
    },
    "Schizophrenia Spectrum and Other Psychotic Disorders": {
        "Schizophrenia": {
            "positive_symptoms": [
                {"name": "Delusions", "code": "N1", "criterion": "A", "required": True},
                {"name": "Hallucinations", "code": "N2", "criterion": "A", "required": True},
                {"name": "Disorganized speech", "code": "N3", "criterion": "A"},
            ],
            "negative_symptoms": [
                {"name": "Grossly disorganized or catatonic behavior", "code": "N4", "criterion": "A"},
                {"name": "Negative symptoms (diminished emotional expression or avolition)", "code": "N5", "criterion": "A"},
            ],
            "functional_decline": [
                {"name": "Significant decline in functioning", "code": "N6", "criterion": "B", "required": True}
            ],
            "duration_requirement": "6 months",
            "exclusion_criteria": [
                "Substance/medical condition effects excluded",
                "Autism spectrum disorder/communication disorder excluded"
            ]
        },
        "Brief Psychotic Disorder": {
            "psychotic_symptoms": [
                {"name": "Delusions", "code": "O1"},
                {"name": "Hallucinations", "code": "O2"},
                {"name": "Disorganized speech", "code": "O3"},
                {"name": "Grossly disorganized or catatonic behavior", "code": "O4"},
            ],
            "duration_requirement": "At least 1 day but less than 1 month",
            "return_to_functioning": "Eventually returns to normal functioning",
            "specifiers": [
                "With marked stressor(s)",
                "Without marked stressor(s)",
                "With postpartum onset"
            ]
        }
    }
}

# Clinical assessment scales and their score interpretations
CLINICAL_SCALES = {
    "PHQ-9": {
        "name": "Patient Health Questionnaire-9",
        "description": "Depression severity assessment",
        "scoring": {
            "0-4": "Minimal depression",
            "5-9": "Mild depression", 
            "10-14": "Moderate depression",
            "15-19": "Moderately severe depression",
            "20-27": "Severe depression"
        }
    },
    "GAD-7": {
        "name": "Generalized Anxiety Disorder 7-item",
        "description": "Anxiety severity assessment",
        "scoring": {
            "0-4": "Minimal anxiety",
            "5-9": "Mild anxiety",
            "10-14": "Moderate anxiety", 
            "15-21": "Severe anxiety"
        }
    },
    "PCL-5": {
        "name": "PTSD Checklist for DSM-5",
        "description": "PTSD symptom assessment",
        "scoring": {
            "0-30": "Low PTSD symptoms",
            "31-32": "Probable PTSD (cutoff score)",
            "33-80": "High PTSD symptoms"
        }
    },
    "ADHD-RS": {
        "name": "ADHD Rating Scale",
        "description": "ADHD symptom severity",
        "scoring": {
            "0-25": "Normal range",
            "26-35": "Mild symptoms",
            "36-45": "Moderate symptoms",
            "46-54": "Severe symptoms"
        }
    }
}

# Severity specifiers used across disorders
SEVERITY_LEVELS = [
    "Minimal",
    "Mild", 
    "Moderate",
    "Severe",
    "Extreme"
]

# Common frequency descriptors
FREQUENCY_OPTIONS = [
    "Never",
    "Rarely", 
    "Sometimes",
    "Often",
    "Very often",
    "Daily",
    "Multiple times per day",
    "Weekly",
    "Monthly"
]

# Duration descriptors
DURATION_OPTIONS = [
    "Less than 1 week",
    "1-2 weeks",
    "2-4 weeks", 
    "1-3 months",
    "3-6 months",
    "6-12 months",
    "1-2 years",
    "More than 2 years"
]

# Functional impairment domains
IMPAIRMENT_DOMAINS = [
    "Work/School",
    "Social relationships",
    "Family relationships", 
    "Daily living activities",
    "Self-care",
    "Recreation/Leisure"
]