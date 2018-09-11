# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from shutil import move


class PepperfryImagesPipeline(ImagesPipeline):
    # def process_item(self, item, spider):
        # import ipdb
        # ipdb.set_trace()
        # self.image_store = spider.settings.get('IMAGES_STORE')
        # return item

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

            # if not os.rename(path, target_path):
            #     raise DropItem("Could not move image to target folder")

        if self.IMAGES_RESULT_FIELD in item.fields:
            item[self.IMAGES_RESULT_FIELD] = [x for ok, x in results if ok]
        return item
