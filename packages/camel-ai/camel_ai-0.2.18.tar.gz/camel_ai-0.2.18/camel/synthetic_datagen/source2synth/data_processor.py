# ========= Copyright 2023-2024 @ CAMEL-AI.org. All Rights Reserved. =========
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ========= Copyright 2023-2024 @ CAMEL-AI.org. All Rights Reserved. =========

import random
from typing import Any, Dict, List, Optional, Sequence

import numpy as np
from tqdm import tqdm

from camel.agents.multi_hop_generator_agent import MultiHopGeneratorAgent
from camel.logger import get_logger
from camel.synthetic_datagen.source2synth.user_data_processor_config import (
    ProcessorConfig,
)

logger = get_logger(__name__)


class UserDataProcessor:
    r"""User Data Processor."""

    def __init__(self, config: Optional[ProcessorConfig] = None):
        self.config = config or ProcessorConfig()
        random.seed(self.config.seed)
        np.random.seed(self.config.seed)
        self.multi_hop_agent = (
            MultiHopGeneratorAgent() if self.config.use_ai_model else None
        )

    def process_text(
        self, text: str, source: str = "user_input"
    ) -> List[Dict[str, Any]]:
        r"""Process a single text."""
        # Convert text to standard format
        raw_data = [
            {
                'text': text,
                'source': source,
            }
        ]

        # Construct examples
        constructor = ExampleConstructor(self.config, self.multi_hop_agent)
        examples = constructor.construct_examples(raw_data)

        # Manage data
        curator = DataCurator(self.config)
        final_dataset = curator.curate_dataset(examples)

        return final_dataset

    def process_batch(
        self, texts: List[str], sources: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        r"""Process multiple texts in batch."""
        if sources is None:
            sources = ["user_input"] * len(texts)
        elif len(sources) != len(texts):
            raise ValueError("Length of sources must match length of texts")

        raw_data = [
            {
                'text': text,
                'source': source,
            }
            for text, source in zip(texts, sources)
        ]

        # Construct examples
        constructor = ExampleConstructor(self.config, self.multi_hop_agent)
        examples = constructor.construct_examples(raw_data)

        # Manage data
        curator = DataCurator(self.config)
        final_dataset = curator.curate_dataset(examples)

        return final_dataset


class ExampleConstructor:
    r"""Example Constructor."""

    def __init__(
        self,
        config: ProcessorConfig,
        multi_hop_agent: Optional[MultiHopGeneratorAgent] = None,
    ):
        self.config = config
        self.multi_hop_agent = multi_hop_agent

    def construct_examples(
        self, raw_data: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        r"""Construct training examples."""
        logger.info("Starting to construct training examples...")
        examples = []

        for data in tqdm(raw_data, desc="Constructing examples"):
            # 1. Text preprocessing
            processed_text = self._preprocess_text(data.get('text', ''))
            if not processed_text:
                continue

            # 2. Generate key information pairs
            info_pairs = self._extract_info_pairs(processed_text)

            # 3. Construct question-answer pairs
            qa_pairs = self._generate_qa_pairs(info_pairs)

            # 4. Add metadata
            example = {
                'text': processed_text,
                'qa_pairs': qa_pairs,
                'metadata': {
                    'source': data.get('source', 'unknown'),
                    'timestamp': data.get('timestamp', ''),
                    'complexity': self._calculate_complexity(qa_pairs),
                },
            }

            examples.append(example)

        logger.info(f"Successfully constructed {len(examples)} examples")
        return examples

    def _preprocess_text(self, text: str) -> str:
        r"""Text preprocessing."""
        if not isinstance(text, str):
            return ''

        # 1. Basic cleaning
        text = text.strip()

        # 2. Length check
        if (
            len(text) < self.config.min_length
            or len(text) > self.config.max_length
        ):
            return ''

        # 3. Quality check
        if not self._check_text_quality(text):
            return ''

        return text

    def _check_text_quality(self, text: str) -> bool:
        r"""Check text quality."""
        # 1. Basic quality check
        if text.count('.') < 2:  # Must have at least 2 sentences
            return False

        # 2. Special character ratio check
        special_char_ratio = len(
            [c for c in text if not c.isalnum() and not c.isspace()]
        ) / len(text)
        if special_char_ratio > 0.3:  # No more than 30% special characters
            return False

        return True

    def _extract_info_pairs(self, text: str) -> List[Dict[str, Sequence[str]]]:
        r"""Extract information pairs and relationships."""
        # Split into sentences
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        info_pairs = []

        # Extract combinations of multiple related sentences
        for i in range(len(sentences) - 2):
            if len(sentences[i]) > 10 and len(sentences[i + 1]) > 10:
                info_pairs.append(
                    {
                        'premise': sentences[i],
                        'intermediate': sentences[i + 1],
                        'conclusion': sentences[i + 2]
                        if i + 2 < len(sentences)
                        else '',
                        'related_contexts': [
                            s
                            for j, s in enumerate(sentences)
                            if j != i and j != i + 1 and len(s) > 10
                        ][:2],
                        # Limit to 2 additional related contexts
                    }
                )

        return info_pairs

    def _generate_qa_pairs(
        self, info_pairs: List[Dict[str, Sequence[str]]]
    ) -> List[Dict[str, str]]:
        r"""Generate multi-hop question-answer pairs."""
        qa_pairs = []

        for pair in info_pairs:
            # 1. Generate multi-hop question-answer pair using AI
            if self.multi_hop_agent:
                # Construct full context
                context = (
                    f"{pair['premise']}. {pair['intermediate']}."
                    f" {pair['conclusion']}"
                )
                response = self.multi_hop_agent.generate_multi_hop_qa(context)
                if response:
                    qa_pairs.append(response.value.dict())
                    continue

        return qa_pairs

    def _calculate_complexity(self, qa_pairs: List[Dict[str, Any]]) -> float:
        r"""Calculate complexity of QA pairs."""
        if not qa_pairs:
            return 0.0

        # Calculate complexity based on multiple factors
        complexities = []
        for qa in qa_pairs:
            # 1. Number of reasoning steps
            reasoning_steps_count = len(qa.get('reasoning_steps', []))

            # 2. Number of supporting facts
            supporting_facts_count = len(qa.get('supporting_facts', []))

            # 3. Question length
            question_length = len(qa['question'].split())

            # 4. Answer length
            answer_length = len(qa['answer'].split())

            # Calculate complexity of a single QA pair
            qa_complexity = (
                min(reasoning_steps_count / 3, 1.0)
                * 0.4  # Weight for reasoning steps
                + min(supporting_facts_count / 3, 1.0)
                * 0.3  # Weight for supporting facts
                + min(question_length / 20, 1.0)
                * 0.15  # Weight for question length
                + min(answer_length / 50, 1.0) * 0.15
                # Weight for answer length
            )

            complexities.append(qa_complexity)

        return sum(complexities) / len(complexities)


class DataCurator:
    r"""Data Manager."""

    def __init__(self, config: ProcessorConfig):
        self.config = config

    def curate_dataset(
        self, examples: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        r"""Dataset management."""
        logger.info("Starting dataset management...")

        # 1. Quality filtering
        quality_filtered = self._quality_filter(examples)
        logger.info(
            f"Remaining examples after quality filtering:"
            f" {len(quality_filtered)}"
        )

        # 2. Complexity filtering
        complexity_filtered = self._complexity_filter(quality_filtered)
        logger.info(
            f"Remaining examples after complexity filtering:"
            f" {len(complexity_filtered)}"
        )

        # 3. Deduplication
        deduplicated = self._remove_duplicates(complexity_filtered)
        logger.info(
            f"Remaining examples after deduplication: {len(deduplicated)}"
        )

        # 4. Sample to target size
        final_dataset = self._sample_dataset(deduplicated)
        logger.info(f"Final dataset size: {len(final_dataset)}")

        return final_dataset

    def _quality_filter(
        self, examples: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        r"""Quality filtering."""
        filtered = []

        for example in examples:
            # 1. Check QA pair quality
            qa_quality = self._check_qa_quality(example.get('qa_pairs', []))

            # 2. Check text quality
            text_quality = (
                len(example.get('text', '').split()) >= 20
            )  # At least 20 words

            if qa_quality and text_quality:
                filtered.append(example)

        return filtered

    def _check_qa_quality(self, qa_pairs: List[Dict[str, str]]) -> bool:
        r"""Check quality of QA pairs."""
        if not qa_pairs:
            return False

        for qa in qa_pairs:
            # 1. Length check
            if (
                len(qa.get('question', '')) < 10
                or len(qa.get('answer', '')) < 5
            ):
                return False

            # 2. QA pair duplication check
            if qa.get('question', '') == qa.get('answer', ''):
                return False

        return True

    def _complexity_filter(
        self, examples: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        r"""Complexity filtering."""
        return [
            example
            for example in examples
            if example.get('metadata', {}).get('complexity', 0)
            >= self.config.complexity_threshold
        ]

    def _remove_duplicates(
        self, examples: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        r"""Remove duplicates."""
        seen = set()
        unique_examples = []

        for example in examples:
            # Use text and QA pair combination as unique identifier
            text = example.get('text', '')
            qa_str = str(example.get('qa_pairs', []))

            identifier = hash(text + qa_str)

            if identifier not in seen:
                seen.add(identifier)
                unique_examples.append(example)

        return unique_examples

    def _sample_dataset(
        self, examples: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        r"""Sample to target dataset size."""
        if len(examples) <= self.config.dataset_size:
            return examples

        return random.sample(examples, self.config.dataset_size)
