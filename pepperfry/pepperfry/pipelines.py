# -*- coding: utf-8 -*-

import os
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from shutil import move


class PepperfryImagesPipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        self.image_store = 'images_store'
        target_dir = item['item_dir']
        os.makedirs(target_dir, exist_ok=True)
        for i, result in enumerate([x for ok, x in results if ok], 1):
            path = result['path']
            path = os.path.join(self.image_store, path)

            image_name = 'im_{}.jpg'.format(i)
            target_path = os.path.join(target_dir, image_name)

            move(path, target_path)

        if self.IMAGES_RESULT_FIELD in item.fields:
            item[self.IMAGES_RESULT_FIELD] = [x for ok, x in results if ok]
        return item
