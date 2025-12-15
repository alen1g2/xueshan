import random


class ValueJourneyGame:
    def __init__(self):
        self.player_name = ""
        self.score = 0
        self.knowledge_points = 0
        self.current_scene = 0
        self.current_question = 0
        self.choices_made = []
        self.mode = "scene"  # "scene", "knowledge", "summary"

        # 静态数据：核心价值原则
        self.VALUE_PRINCIPLES = {
            "集体主义": "自觉遵循社会发展客观规律，将集体利益置于个人利益之上。",
            "理性消费": "树立正确的消费观，做到量入为出、适度消费，不盲目攀比。",
            "社会责任": "正确处理个人与社会的关系，积极承担社会责任，实现人生价值。",
            "生态文明": "树立生态文明观念，以实际行动践行绿色发展理念。"
        }

        # 静态数据：场景
        self.scenes = [
            {
                "title": "🏫 校园生活场景：集体与公平",
                "description": "你是一名高中生，面临班级事务中的公正选择...",
                "question": "班级选举班干部，你的好朋友虽然能力一般但很想当选，另一位同学能力很强但不太熟。你会如何投票？",
                "options": [
                    {"text": "投给好朋友，因为友情最重要", "value": 0,
                     "feedback": "❌ 价值分析：这是个人情感驱动的选择。友情固然重要，但作为公民，我们做价值判断和价值选择时，应把集体利益和公平公正放在首位。",
                     "principle": "集体主义"},
                    {"text": "投给能力强的同学，为了班级发展", "value": 1,
                     "feedback": "✅ 价值分析：正确！这体现了自觉遵循社会发展客观规律，把集体利益放在首位，是正确的集体主义价值观。",
                     "principle": "集体主义"},
                    {"text": "弃权，不想得罪任何人", "value": 0,
                     "feedback": "❌ 价值分析：逃避不是解决问题的办法。正确的价值选择要求我们勇于做出判断和承担责任。",
                     "principle": "集体主义"}
                ]
            },
            {
                "title": "🛒 消费选择场景：理性与攀比",
                "description": "周末和同学去商场购物，面对物质诱惑...",
                "question": "看到一件很贵的名牌衣服，同学们都在买，但你的家庭条件一般。你会？",
                "options": [
                    {"text": "借钱也要买，不能被同学看不起", "value": 0,
                     "feedback": "❌ 价值分析：盲目攀比是不理性的消费观，容易陷入债务困境。正确的消费观要求我们量入为出、适度消费。",
                     "principle": "理性消费"},
                    {"text": "选择适合自己经济能力的衣服", "value": 1,
                     "feedback": "✅ 价值分析：正确！这体现了理性的消费观，符合正确的价值观，是自尊自信的表现。",
                     "principle": "理性消费"},
                    {"text": "让父母买，满足自己的愿望", "value": 0,
                     "feedback": "❌ 价值分析：缺乏感恩和体谅之心。我们应该树立正确的消费观念，并尊重和体谅父母。",
                     "principle": "理性消费"}
                ]
            }
        ]

        # 静态数据：知识点
        self.knowledge_questions = [
            {
                "question": "价值观的基本特征是？",
                "options": ["主观性、历史性、社会性", "客观性、永恒性、个人性", "随意性、变化性、相对性"],
                "correct": 0,
                "theory": "价值观具有历史性、社会性、主观性和多变性。"
            },
            {
                "question": "价值判断和价值选择的关系是？",
                "options": ["价值判断决定价值选择", "价值选择决定价值判断", "两者相互影响、相互制约"],
                "correct": 2,
                "theory": "价值判断是价值选择的基础，正确的价值判断才能做出正确的价值选择。"
            },
            {
                "question": "社会主义核心价值观中，属于**社会层面**的是？",
                "options": ["富强、民主、文明、和谐", "自由、平等、公正、法治", "爱国、敬业、诚信、友善"],
                "correct": 1,
                "theory": "核心价值观的三个层面：国家层面（富强、民主、文明、和谐），社会层面（自由、平等、公正、法治），个人层面（爱国、敬业、诚信、友善）。"
            }
        ]

    # --- 新增的方法：序列化与反序列化 ---
    def to_dict(self):
        """将当前动态状态转换为字典，以便存入 session"""
        return {
            "player_name": self.player_name,
            "score": self.score,
            "knowledge_points": self.knowledge_points,
            "current_scene": self.current_scene,
            "current_question": self.current_question,
            "choices_made": self.choices_made,
            "mode": self.mode
        }

    def load_from_dict(self, data):
        """从字典中恢复状态"""
        if not data:
            return
        self.player_name = data.get("player_name", "")
        self.score = data.get("score", 0)
        self.knowledge_points = data.get("knowledge_points", 0)
        self.current_scene = data.get("current_scene", 0)
        self.current_question = data.get("current_question", 0)
        self.choices_made = data.get("choices_made", [])
        self.mode = data.get("mode", "scene")

    # ----------------------------------

    def get_current_data(self):
        if self.mode == "scene":
            if self.current_scene >= len(self.scenes):
                self.mode = "knowledge"
                return self.get_current_data()

            scene = self.scenes[self.current_scene]
            return {
                "type": "scene",
                "scene_id": self.current_scene,
                "title": scene['title'],
                "description": scene['description'],
                "question": scene['question'],
                "options": [opt['text'] for opt in scene['options']]
            }

        elif self.mode == "knowledge":
            if self.current_question >= len(self.knowledge_questions):
                self.mode = "summary"
                return self.get_current_data()

            q = self.knowledge_questions[self.current_question]
            return {
                "type": "knowledge",
                "question_id": self.current_question,
                "question": q['question'],
                "options": q['options']
            }

        elif self.mode == "summary":
            return self._get_summary_data()

        return {"type": "finished"}

    def handle_scene_choice(self, choice_index):
        scene = self.scenes[self.current_scene]
        option = scene['options'][choice_index]
        is_correct = option['value'] == 1

        feedback_data = {
            "is_correct": is_correct,
            "choice_text": option['text'],
            "feedback": option['feedback'],
            "principle": option['principle'],
            "theory": self.VALUE_PRINCIPLES.get(option['principle'], '')
        }

        if is_correct:
            self.score += 1
            self.knowledge_points += 10

        self.choices_made.append({
            "scene": scene['title'],
            "choice": option['text'],
            "correct": is_correct
        })

        self.current_scene += 1
        return feedback_data

    def handle_knowledge_choice(self, choice_index):
        q = self.knowledge_questions[self.current_question]
        is_correct = choice_index == q['correct']

        feedback_data = {
            "is_correct": is_correct,
            "choice_text": q['options'][choice_index],
            "correct_text": q['options'][q['correct']],
            "theory": q['theory']
        }

        if is_correct:
            self.knowledge_points += 10

        self.current_question += 1
        return feedback_data

    def _get_summary_data(self):
        final_score = self.score * 20 + self.knowledge_points
        total_possible = len(self.scenes) * 20 + len(self.knowledge_questions) * 10
        percentage = (final_score / total_possible) * 100 if total_possible > 0 else 0

        if percentage >= 85:
            evaluation = "🌟 优秀！你已形成正确的价值判断和选择能力。"
        elif percentage >= 65:
            evaluation = "👍 良好！你对核心知识有所掌握，但部分情景选择还需加强。"
        else:
            evaluation = "💪 加油！建议复习第六课内容，加深对价值观的理解。"

        return {
            "type": "summary",
            "player_name": self.player_name,
            "score": self.score,
            "knowledge_points": self.knowledge_points,
            "final_score": final_score,
            "total_possible": total_possible,
            "percentage": round(percentage, 1),
            "evaluation": evaluation,
            "choices_made": self.choices_made
        }