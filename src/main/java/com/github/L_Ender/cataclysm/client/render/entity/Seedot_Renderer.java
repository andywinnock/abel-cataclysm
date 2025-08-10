package com.github.L_Ender.cataclysm.client.render.entity;

import com.github.L_Ender.cataclysm.Cataclysm;
import com.github.L_Ender.cataclysm.client.model.CMModelLayers;
import com.github.L_Ender.cataclysm.client.model.entity.Seedot_Model;
import com.github.L_Ender.cataclysm.entity.Pet.Seedot_Entity;
import com.mojang.blaze3d.vertex.PoseStack;
import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.client.renderer.entity.MobRenderer;
import net.minecraft.resources.ResourceLocation;
import net.minecraftforge.api.distmarker.Dist;
import net.minecraftforge.api.distmarker.OnlyIn;

@OnlyIn(Dist.CLIENT)
public class Seedot_Renderer extends MobRenderer<Seedot_Entity, Seedot_Model> {

    private static final ResourceLocation SEEDOT_TEXTURE = new ResourceLocation(Cataclysm.MODID, "textures/entity/seedot.png");

    public Seedot_Renderer(EntityRendererProvider.Context renderManagerIn) {
        super(renderManagerIn, new Seedot_Model(renderManagerIn.bakeLayer(CMModelLayers.SEEDOT_MODEL)), 0.3F);
    }

    @Override
    public ResourceLocation getTextureLocation(Seedot_Entity entity) {
        return SEEDOT_TEXTURE;
    }

    @Override
    protected void scale(Seedot_Entity entitylivingbaseIn, PoseStack matrixStackIn, float partialTickTime) {
        matrixStackIn.scale(0.8F, 0.8F, 0.8F);
    }
}