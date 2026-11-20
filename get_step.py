import json

with open(r'C:\Users\91861\.gemini\antigravity\brain\821c98cc-7767-421b-b10e-3565795f6465\.system_generated\logs\transcript_full.jsonl', encoding='utf-8') as f:
    for line in f:
        obj = json.loads(line)
        if obj.get('step_index') in [874, 875, 876]:
            print(f"=== STEP {obj.get('step_index')} ===")
            tc = obj.get('tool_calls')
            if tc:
                for c in tc:
                    print("Tool:", c.get('name'))
                    args = c.get('args', {})
                    for k, v in args.items():
                        print(f"  {k}: {str(v)[:150]}...")
                        if k == 'Content':
                            with open('recovered_render.py', 'w', encoding='utf-8') as rf:
                                rf.write(v)
                            print("Saved to recovered_render.py!")
